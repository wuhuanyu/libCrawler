# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from stacklib.item import CNNItem as CNN
from time import time
from scrapy.loader import ItemLoader
from scrapy import Request


class CnnSpider(CrawlSpider):
    source = 'cnn'
    crawled_at = int(round(time() * 1000))

    name = 'cnn'
    allowed_domains = ['edition.cnn.com']
    start_urls = ['http://edition.cnn.com']
    base_url = start_urls[0]

    url_tags = {
        '/INTERNATIONAL': 'business',
        '/entertainment': 'entertainment',
        '/asia': 'world',
        '/china': 'china',
        '/us': 'world',
        '/techonology': 'tech',
        '/sport': 'sport',
        '/travel': 'travel',
        '/health': 'health',
    }

    def busi_list(self, res):
        urls = res.xpath('.//a[re:test(@href,"^/\d{4}/\d{2}/\d{2}/.*$")]')
        


        pass

    def ent_list(self, res):
        pass

    def asia_list(self, res):
        pass

    def china_list(self, res):
        pass

    def us_list(self, res):
        pass

    def tech_list(self, res):
        pass

    def sport_list(self, res):
        pass

    def travel_list(self, res):
        pass

    def health_list(self, res):
        pass

    def start_requests(self):
        for url, tag in self.url_tags:
            if url == '/INTERNATIONAL':
                callback = self.busi_list
            if url == '/entertainment':
                callback = self.ent_list
            if url == '/aisa':
                callback = self.asia_list
            if url == '/china':
                callback = self.china_list
            if url == '/us':
                callback = self.us_list
            if url == '/technology':
                callback = self.tech_list
            if url == '/sport':
                callback = self.sport_list

            if url == '/travel':
                callback = self.travel_list
            if url == '/health':
                callback = self.health_list
            
            yield Request(url=self.base_url+url,callback=callback,meta={'tag':tag})
