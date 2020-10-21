import json
from datetime import date

from kingfisher_scrapy.base_spider import IndexSpider
from kingfisher_scrapy.util import components, date_range_by_month, handle_http_error


class ChileCompraBaseSpider(IndexSpider):
    custom_settings = {
        'DOWNLOAD_FAIL_ON_DATALOSS': False,
    }

    limit = 100
    base_list_url = 'https://apis.mercadopublico.cl/OCDS/data/listaA%C3%B1oMes/{0.year:d}/{0.month:02d}/{1}/{2}'
    formatter = staticmethod(components(-4, -1))
    count_pointer = '/pagination/total'
    yield_list_results = False

    def start_requests(self):
        today = date.today()
        if hasattr(self, 'year'):
            year = int(self.year)
            start = date(year, 1, 1)
            stop = date(year, 12, 1)
            if year == today.year:
                stop = stop.replace(month=today.month)
        else:
            start = date(2008, 1, 1)
            stop = today

        for d in date_range_by_month(start, stop):
            yield self.build_request(
                self.base_list_url.format(d, 0, self.limit),
                formatter=components(-4, -1),
                meta={
                    'year': d.year,
                    'month': d.month,
                },
                callback=self.parse_list
            )

    @handle_http_error
    def parse_list(self, response, **kwargs):
        data = json.loads(response.text)
        # Some files contain invalid packages, e.g.:
        # {
        #   "status": 500,
        #   "detail": "error"
        # }
        if 'status' in data and data['status'] != 200:
            data['http_code'] = data['status']
            yield self.build_file_error_from_response(response, errors=data)
            return

        kwargs['callback'] = self.parse_items
        yield from super().parse_list(response, **kwargs)
        yield from self.parse_items(response)

    def parse_items(self, response):
        data = json.loads(response.text)
        for item in data['data']:
            # An item looks like:
            #
            # {
            #   "ocid": "ocds-70d2nz-2359-2-LE19",
            #   "urlTender": "https://apis.mercadopublico.cl/OCDS/data/tender/2359-2-LE19",
            #   "urlAward": "https://apis.mercadopublico.cl/OCDS/data/award/2359-2-LE19",
            #   "urlPlanning": "https://apis.mercadopublico.cl/OCDS/data/planning/2359-2-LE19"
            # }
            yield from self.handle_item(item)

    def url_builder(self, value, data, response):
        year = response.request.meta['year']
        month = response.request.meta['month']

        return self.base_list_url.format(date(year, month, 1), value, self.limit)
