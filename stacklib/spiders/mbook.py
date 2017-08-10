# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy import Request as Re


class MillionBookSpider(CrawlSpider):
    name = 'mbook'
    allowed_domains = ['themillions.com']
    start_urls = ['http://themillions.com']

    book_sub_url ='/book-reviews'

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def start_requests(self):
        yield Re(url = self.start_urls[0]+self.book_sub_url,callback=self.book_list)
        
        
    def book_list(self,res):
        urls = res.css('.bookimages').xpath('.//li/a/@href').extract()

        for url in urls:
            yield Re(url=self.start_urls[0]+self.book_sub_url,callback=self.parse_book) 
        
    
    def parse_book(self,res):
        

        





    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
