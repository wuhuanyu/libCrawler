# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from stacklib.item import medium_item as MediumItem
from time import time


class MediumSpider(CrawlSpider):
    name = 'medium'
    allowed_domains = ['medium.com']
    start_urls = ['https://medium.com/']

    source = 'medium'
    crawled_at =int(round(time())*1000)


    def start_requests(self):
        
        pass
    
    def parse_list(self,res):
    
    def parse_art(self,res):



