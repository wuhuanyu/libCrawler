# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from w3lib.html import remove_tags
from scrapy.loader.processors import Join, MapCompose, TakeFirst


class NewsBaseItem(scrapy.Item):
    '''
     Base Cls for newsItem
    '''
    source = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    summary = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
    timestamp = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )

    crawled_at = scrapy.Field(
        output_processor=TakeFirst()
    )
    image_urls = scrapy.Field()
    images = scrapy.Field()
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    text = scrapy.Field(input_processor=MapCompose(remove_tags))


class BBCItem(NewsBaseItem):
    tag = scrapy.Field(output_processor=TakeFirst())

# define the fields for your item here like:
# name = scrapy.Field()

class ReutersItem(NewsBaseItem):
    tag = scrapy.Field(output_processor=TakeFirst())

class CNNItem(NewsBaseItem):
    tag = scrapy.Field(output_processor=TakeFirst())