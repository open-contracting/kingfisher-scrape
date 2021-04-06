import scrapy

from kingfisher_scrapy.base_spider import SimpleSpider
from kingfisher_scrapy.util import components, handle_http_error


class CostaRicaPoderJudicialRecords(SimpleSpider):
    """
    Domain
      Poder Judicial de Costa Rica
    Spider arguments
      from_date
        Download only data from this year onward (YYYY format). Defaults to '2018'.
      until_date
        Download only data until this year (YYYY format). Defaults to the current year.
    Bulk download documentation
      http://datosabiertospj.eastus.cloudapp.azure.com/dataset/estandar-de-datos-de-contrataciones-abiertas-ocds
    """
    name = 'costa_rica_poder_judicial_records'

    # BaseSpider
    skip_pluck = 'Already covered (see code for details)'  # costa_rica_poder_judicial_releases

    # SimpleSpider
    data_type = 'record_package'
    date_format = 'year'
    default_from_date = '2018'

    def start_requests(self):
        url = 'http://datosabiertospj.eastus.cloudapp.azure.com/api/3/action/package_show?id=estandar-de-datos-de' \
              '-contrataciones-abiertas-ocds'
        yield scrapy.Request(url, meta={'file_name': 'list.json'}, callback=self.parse_list)

    @handle_http_error
    def parse_list(self, response):
        data = response.json()
        for resource in data['result']['resources']:
            if resource['format'].upper() == 'JSON':
                if self.from_date and self.until_date:
                    # URL looks like:
                    # https://pjcrdatosabiertos.blob.core.windows.net/datosabiertos/OpenContracting/2021.json
                    year = int(components(-1)(resource['url']))
                    if not (self.from_date.year <= year <= self.until_date.year):
                        continue
                yield self.build_request(resource['url'], formatter=components(-1))
