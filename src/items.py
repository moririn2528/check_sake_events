# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EventItem(scrapy.Item):
    event_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()


class OtherItem(scrapy.Item):
    url = scrapy.Field()
