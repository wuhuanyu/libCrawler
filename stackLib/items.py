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
    # category = scrapy.Field(output_processor=TakeFirst())
    # tag = scrapy.Field(output_processor=TakeFirst())
    image_urls = scrapy.Field()
    images = scrapy.Field()
    text = scrapy.Field(input_processor=MapCompose(remove_tags))


class BBCItem(NewsBaseItem):


'''
BBCItem
'''
    tag = scrapy.Field(output_processor=TakeFirst())

# define the fields for your item here like:
# name = scrapy.Field()
