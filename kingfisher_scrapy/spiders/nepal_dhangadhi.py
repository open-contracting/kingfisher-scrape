import scrapy

from kingfisher_scrapy.base_spider import SimpleSpider
from kingfisher_scrapy.util import components, handle_http_error


class NepalDhangadhi(SimpleSpider):
    """
    Domain
      Dhangadhi Infrastructure Management System (IMS)
    Caveats
      Some URLs listed in https://admin.ims.susasan.org/api/static-data/dhangadhi require login and cannot be
      downloaded
    Bulk download documentation
      https://ims.susasan.org/dhangadhi/about
    """
    name = 'nepal_dhangadhi'

    # SimpleSpider
    data_type = 'release_package'

    def start_requests(self):
        yield scrapy.Request(
            'https://admin.ims.susasan.org/api/static-data/dhangadhi',
            meta={'file_name': 'list.json'},
            callback=self.parse_list,
        )

    @handle_http_error
    def parse_list(self, response):
        pattern = 'https://admin.ims.susasan.org/ocds/json/dhangadhi-{}.json'
        data = response.json()
        for item in reversed(data['data']['fiscal_years']):
            # A URL might redirect to https://admin.ims.susasan.org/login
            yield self.build_request(pattern.format(item['name']), formatter=components(-1),
                                     meta={'dont_redirect': True})
