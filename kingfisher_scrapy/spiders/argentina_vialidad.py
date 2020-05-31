import scrapy

from kingfisher_scrapy.base_spider import SimpleSpider


class ArgentinaVialidad(SimpleSpider):
    """
    API documentation
      https://datosabiertos.vialidad.gob.ar/ui/index.html#!/datos_abiertos
    Spider arguments
      sample
        Download one set of releases.
    """
    name = 'argentina_vialidad'
    data_type = 'release_package_list'

    def start_requests(self):
        yield scrapy.Request(
            'https://datosabiertos.vialidad.gob.ar/api/ocds/package/all',
            meta={'kf_filename': 'all.json'}
        )
