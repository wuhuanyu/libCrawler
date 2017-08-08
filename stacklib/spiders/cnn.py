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
        tag = res.meta['tag']
        urls = res.xpath(
            './/a[re:test(@href,"^/\d{4}/\d{2}/\d{2}/.*$")]').extract()
        if not len(urls) == 0:
            for url in urls:
                yield Request(self.base_url + url, callback=self.parse_busi_art, meta={'tag': tag})

        urls_ = res.xpath(
            './/a[re:test(@href,"http://money.cnn.com/\d{4}/\d{2}/\d{2}/.*$")]').extract()
        if not len(urls_) == 0:
            for url in urls_:
                yield Request(self.base_url + url, callback=self.parse_busi_art, meta={'tag': tag})

    def parse_busi_art(self, res):
        pass

    def ent_list(self, res):
        tag = res.meta['tag']
        urls = res.xpath(
            './/a[re:test(@href,"^/\d{4}/\d{2}/\d{2}/.*$")]').extract()
        if not len(urls) == 0:
            for url in urls:
                yield Request(self.base_url + url, callback=self.parse_ent_art, meta={'tag': tag})

        pass

    def parse_ent_art(self, res):

        # http://edition.cnn.com/2017/08/08/entertainment/taylor-swift-lawsuit-court-rules/index.html
        url = res.url
        tag = res.meta['tag']
        art = res.xpath(
            './/div[@class="l-container"]//*[@class="pg-rail-tall__wrapper"]')
        ci = ItemLoader(item=CNN(), selector=art)

        ci.add_value('crawled_at', self.crawled_at)
        ci.add_value('tag', tag)
        ci.add_value('url', url)
        ci.add_value('source', self.source)

        ci.add_xpath('title', './/div[@class="pg-headline"]/text()')
        ci.add_xpath(
            'timestamp', './/div[@class="metadata"]//p[@class="update-time"]/text()')

        # ci.add_xpath('text','.//div[@class="pg-rail-tall__body"]//div[@class="el__leafmedia el__leafmedia--sourced-paragraph"]|div[@class="el__leafmedia el__leafmedia--sourced-paragraph"]|div[@class=""]')
        ci.add_css('text', '.zn-body__paragraph::text')

        image_ = res.xpath(
            './/div[@class="media__video--thumbnail"]//img/@data-src-medium').extract()

        if image_ is not None and (not len(image_) == 0):
            if not image_.startswith('http'):
                image_ ='http:'+image_
            
            ci.add_value('image_urls',[image_])
        

        return ci.load_item()

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

            yield Request(url=self.base_url + url, callback=callback, meta={'tag': tag})
