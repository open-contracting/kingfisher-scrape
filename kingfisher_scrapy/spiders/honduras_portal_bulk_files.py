import json

import scrapy

from kingfisher_scrapy.base_spider import BaseSpider
from kingfisher_scrapy.util import handle_error


class HondurasPortalBulkFiles(BaseSpider):
    name = 'honduras_portal_bulk_files'

    def start_requests(self):
        yield scrapy.Request(
            'http://www.contratacionesabiertas.gob.hn/api/v1/descargas/?format=json',
            meta={'kf_filename': 'list.json'},
            callback=self.parse_list,
        )

    @handle_error
    def parse_list(self, response):
        filelist = json.loads(response.text)

        if self.sample:
            url = filelist[0]['urls']['json']
            yield scrapy.Request(url, meta={'kf_filename': url.rsplit('/', 1)[-1]})

        else:
            for item in filelist:
                url = item['urls']['json']
                yield scrapy.Request(url, meta={'kf_filename': url.rsplit('/', 1)[-1]})

    @handle_error
    def parse(self, response):
        yield self.build_file_from_response(response, data_type='release_package')
