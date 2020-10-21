from kingfisher_scrapy.base_spider import SimpleSpider
from kingfisher_scrapy.util import components


class NicaraguaSolidWaste(SimpleSpider):
    """
    Spider arguments
      from_date
        Download only data from this date onward (YYYY-MM-DD format).
        If ``until_date`` is provided, defaults to '2000-01-01'.
      until_date
        Download only data until this date (YYYY-MM-DD format).
        If ``from_date`` is provided, defaults to today.
    """
    name = 'nicaragua_solid_waste'
    data_type = 'release_package'
    default_from_date = '2000-01-01'
    date_required = True
    url = 'http://www.gekoware.com/swmp/api/ocds/{}/{}'

    def start_requests(self):
        url = self.url
        # date parameter obtained
        url = url.format(self.from_date.strftime("%Y%m%d"), self.until_date.strftime("%Y%m%d"))
        # url looks like http://www.gekoware.com/swmp/api/ocds/20190101/20201005
        yield self.build_request(url, formatter=components(-2))
