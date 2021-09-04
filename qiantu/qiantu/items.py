# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QiantuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    industry = scrapy.Field()
    job_name = scrapy.Field()
    address = scrapy.Field()
    salary = scrapy.Field()
    company_name = scrapy.Field()
    company_type = scrapy.Field()
    education = scrapy.Field()
    experience = scrapy.Field()
    welfare = scrapy.Field()
