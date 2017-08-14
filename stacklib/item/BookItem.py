import scrapy

from w3lib.html import remove_tags
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from stacklib.item import BaseItem


class Book(BaseItem):
    source = scrapy.Field(output_processor=TakeFirst())

    title = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())

    review_urls = scrapy.Field()

    author = scrapy.Field(input_processor=MapCompose(remove_tags))

    summary = scrapy.Field(input_processor=MapCompose(remove_tags))


class BookReivew(BaseItem):
    book = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())

    title = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    text = scrapy.Field(input_processor=MapCompose(remove_tags))
    comments = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())


class Comment(scrapy.Item):
    author = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())

    text = scrapy.Field(input_processor=MapCompose(remove_tags))
