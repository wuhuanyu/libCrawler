# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from stacklib.item.BlogItem import Medium as M
from time import time


class MediumSpider(CrawlSpider):
    name = 'medium'
    allowed_domains = ['medium.com']
    start_urls = ['https://medium.com/']

    source = 'medium'
    crawled_at =int(round(time())*1000)




    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],callback=self.parse_list)

        
    
    def parse_list(self,res):
        urls = res.xpath('.//a[re:test(@href,"https://medium.com/.*$")]/@href').extract()
        for url in urls:
            yield scrapy.Request(url,callback=self.parse_art)

    
    def parse_art(self,res):

        url = res.url
        main = res.xpath('.//main[@role="main"]')
        mi = scrapy.loader.ItemLoader(item=M(),selector=main)

        mi.add_value('crawled_at',self.crawled_at)
        mi.add_value('url',url)

        img_urls = main.xpath('.//figure//img[@src]/@src').re(r'https://cdn-images.*')

        img_ = [url for url in img_urls if not ('freeze' in url)]
        
        mi.add_value('image_urls',img_)


        # mi.add_xpath('image_urls','.//figure//img[@src]/@src')
        # mi.add_css('image_urls','.graf--title')
        mi.add_css('title','.graf--title')
        mi.add_xpath('text','.//p[re:test(@name,"[0-9a-z]{4}")]')
        
        mi.add_value('source',self.source)

        return mi.load_item()


        # mi.add_xpath('tilte',)








