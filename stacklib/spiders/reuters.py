# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from time import time
from ..items import ReutersItem


def check(arr):
    if type(arr)=='list':
        return len(arr)
    return arr is not None

class ReutersSpider(CrawlSpider):
    name = 'reuters'
    allowed_domains = ['reuters.com']
    start_urls = ['http://reuters.com/']
    source = 'reuters'
    crawled_at = int(round(time() * 1000))

    base_url = start_urls[0]

    url_tags = {
        'finance': 'business',
        'politics': 'politics',
        'news/technology': 'tech',
        'commentary': 'commentary',
        'places/china': 'china',
        'news/us': 'politics',

    }

    def start_request(self):
        for url, tag in self.url_tags.iteritems():
            yield scrapy.Request(self.base_url + url, callback=self.parse_list, meta={'tag': tag})

    def parse_list(self, res):
        tag = res.meta['tag']
        main_panel = res.css('.column1.gridPanel.grid8')
        if not check(main_panel):
            raise Exception('main pannel not found!')
        
        top_sty = main_panel.xpath('.//div[@id="topStory"]')
        
        top_sty_url = top_sty.xpath('.//div[@class="photo"]/a/@href').extract_first()


        

        
        


    def parse_art(self,res):
        pass
    