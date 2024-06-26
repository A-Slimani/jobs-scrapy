# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    salary = scrapy.Field()
    location = scrapy.Field()
    link = scrapy.Field()
    close_date = scrapy.Field()
    website = scrapy.Field()

