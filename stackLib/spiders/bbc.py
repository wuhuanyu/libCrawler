# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

#todo 

class BbcSpider(CrawlSpider):
    name = 'bbc'
    allowed_domains = ['bbc.com/news']
    start_urls = ['http://www.bbc.com/news/']
    url_tags = {
        
    }
    
    
    def start_requests(self):
        


    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    # def parse_item(self, response):
    # i = {}
    # #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
    # #i['name'] = response.xpath('//div[@id="name"]').extract()
    # #i['description'] = response.xpath('//div[@id="description"]').extract()
    # return i
