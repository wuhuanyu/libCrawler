import scrapy

from w3lib.html import remove_tags
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from NewsItem import BaseItem


class BookItem(BaseItem):
    source = scrapy.Field(output_processor=TakeFirst())

    title = scrapy.Field(input_processor=MapCompose(remove_tags),output_processor=TakeFirst())


    review_urls = scrapy.Field()

    author = scrapy.Field(input_processor = MapCompose(remove_tags))

    summary = scrapy.Field(input_processor=MapCompose(remove_tags))





    




    
