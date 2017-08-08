from ..items import NewsBaseItem
from w3lib.html import remove_tags
from scrapy.loader.processors import Join, MapCompose, TakeFirst
import scrapy


class CNNItem(NewsBaseItem):
    tag = scrapy.Field(output_processor=TakeFirst())
