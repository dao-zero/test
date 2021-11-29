# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QiantuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_name = scrapy.Field()
    job_salary = scrapy.Field()
    job_welfare = scrapy.Field()
    job_exp = scrapy.Field()
    address = scrapy.Field()
    # address_small = scrapy.Field()
    people_num = scrapy.Field()
    edu = scrapy.Field()
