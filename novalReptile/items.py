# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookInfoItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    detail = scrapy.Field()
    # pass


class ChapterInfoItem(scrapy.Item):
    title = scrapy.Field()
    name = scrapy.Field()
    content = scrapy.Field()
    index = scrapy.Field()
