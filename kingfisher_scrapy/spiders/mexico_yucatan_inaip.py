from kingfisher_scrapy.base_spider import PeriodicSpider
from kingfisher_scrapy.util import components


class MexicoYucatan(PeriodicSpider):
    """
    Domain
      Instituto Estatal de Transparencia, Acceso a la Información Pública y Protección de Datos Personales
      (INAIP) - Yucatán
    Spider arguments
      from_date
        Download only releases from this date onward (YYYY format).
        If ``from_date`` is not provided defaults to 2020.
      until_date
        Download only releases until this date (YYYY format).
        If ``until_date`` is not provided defaults to 2020.
    API documentation
      https://contratacionesabiertas.inaipyucatan.org.mx/contratacionesabiertas/datosabiertos#
    """
    name = 'mexico_yucatan_inaip'

    # BaseSpider
    root_path = 'arrayReleasePackage.item'
    date_format = 'year'
    default_from_date = '2020'
    default_until_date = '2020'

    # SimpleSpider
    data_type = 'release_package'

    # PeriodicSpider
    pattern = 'https://captura.contratacionesabiertas.inaipyucatan.org.mx/edca/contractingprocess/{}'

    def get_formatter(self):
        return components(-1)