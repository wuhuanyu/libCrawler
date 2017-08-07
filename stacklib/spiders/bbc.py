# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from time import time
from scrapy.loader import ItemLoader

from ..items import BBCItem


class BbcSpider(CrawlSpider):
    name = 'bbc'
    allowed_domains = ['bbc.com']
    start_urls = ['http://www.bbc.com/news/']

    host = 'http://www.bbc.com'
    base_url = start_urls[0]

    crawled_at = int(round(time() * 1000))
    source = 'bbc'

    url_tags = {
        'world': 'politics',
        'world/asia': 'politics',
        'world/africa': 'politics',
        'world/asia/china': 'politics',
        'business': 'business',
        'technology': 'tech',
        'science_and_environment': 'tech',
        'entertainment_and_arts': 'entertainment',
        'health': 'health',
        'special_reports': 'special',
    }

    def start_requests(self):
        # regex = r'world|business|technology|health|science|special'

        for url, tag in self.url_tags.iteritems():
            yield scrapy.Request(self.base_url + url, callback=self.parse_list, meta={'tag': tag})

    def parse_list(self, res):
        tag = res.meta['tag']

        urls = res.xpath('.//a/@href').re(r'/news/.*\d+$')

        if urls is not None:
            for url in urls:
                yield scrapy.Request(url=self.host + url, callback=self.parse_art, meta={'tag': tag})

    def parse_art(self, res):
        page_url = res.url

        # print('pageurl',page_url)
        story_sel = res.xpath('.//div[@class="story-body"]')
        tag = res.meta['tag']
        b = ItemLoader(item=BBCItem(), selector=story_sel)

        b.add_xpath('title', './/h1[@class="storybody__h1"]/text()')
        b.add_xpath(
            'timestamp', './/li[@class="mini-info-list__item"]/div[@data-seconds]/@data-seconds')

        b.add_xpath(
            'image_urls', './/span/img[@class="js-image-replace"]/@src')

        b.add_xpath(
            'summary', './/p[@class="storybody__introduction"]/text()')

        b.add_xpath('text', './/div[@property="articleBody"]/p/text()')

        b.add_value('url', page_url)
        b.add_value('crawled_at', self.crawled_at)
        b.add_value('source', self.source)

        b.add_value('tag', tag)
        return b.load_item()

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), calback='parse_item', follow=True),
    # )

    # def parse_item(self, response):
    # i = {}
    # #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
    # #i['name'] = response.xpath('//div[@id="name"]').extract()
    # #i['description'] = response.xpath('//div[@id="description"]').extract()
    # return i
