# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from stacklib.item.BookItem import BookItem as BItem

from time import time


from scrapy import Request as Re


class MillionBookSpider(CrawlSpider):
    crawled_at = int(round(time()*1000))
    name = 'mbook'
    # allowed_domains = ['themillions.com']
    start_urls = ['http://themillions.com']
    source = 'mbook'

    book_sub_url = '/books-reviews'

    rules = (
        Rule(LinkExtractor(allow=r'Items/'),
             callback='parse_item', follow=True),
    )

    def start_requests(self):
        yield Re(url=self.start_urls[0] + self.book_sub_url, callback=self.book_list)

    def book_list(self, res):
        urls = res.css('.bookimages').xpath('.//li/a/@href').extract()

        for url in urls:
            yield Re(url=self.start_urls[0] + url, callback=self.parse_book)

    def parse_book(self, res):
        url = res.url

        main = res.css('.main-content')

        bi = scrapy.loader.ItemLoader(item=BItem(), selector=main)
        bi.add_value('source', self.source)
        bi.add_value('crawled_at', self.crawled_at)
        bi.add_value('url', url)

        bi.add_xpath('summary', './/div[@class="article"]//p/text()')
        bi.add_xpath('image_urls', './/div[@id="br-book-detail"]//img/@href')
        bi.add_xpath('title', './/div[@id="br-details"]/h1/a/text()')
        bi.add_xpath('author', './/h4/text()')
        bi.add_xpath('review_urls', './/div[@class="article"]/h2/a/@href')
        return bi.load_item()
