import scrapy


class QtuSpider(scrapy.Spider):
    name = 'Qtu'
    allowed_domains = ['www.qiantu.com']
    start_urls = ['http://www.qiantu.com/']

    def parse(self, response):
        pass
