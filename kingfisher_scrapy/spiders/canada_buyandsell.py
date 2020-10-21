from kingfisher_scrapy.base_spider import SimpleSpider
from kingfisher_scrapy.util import components


class CanadaBuyAndSell(SimpleSpider):
    """
    Domain
      Public Works and Government Services Canada
    API documentation
      https://buyandsell.gc.ca/procurement-data/open-contracting-data-standard-pilot/download-ocds-pilot-data
    Caveats
      The dataset is a pilot.
    """
    name = 'canada_buyandsell'
    data_type = 'release_package'
    ocds_version = '1.0'

    def start_requests(self):
        urls = [
            'https://buyandsell.gc.ca/cds/public/ocds/tpsgc-pwgsc_ocds_EF-FY-16-17.json',
            'https://buyandsell.gc.ca/cds/public/ocds/tpsgc-pwgsc_ocds_EF-FY-15-16.json',
            'https://buyandsell.gc.ca/cds/public/ocds/tpsgc-pwgsc_ocds_EF-FY-14-15.json',
            'https://buyandsell.gc.ca/cds/public/ocds/tpsgc-pwgsc_ocds_EF-FY-13-14.json',
        ]

        for url in urls:
            yield self.build_request(url, formatter=components(-1))
