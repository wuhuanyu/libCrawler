# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from time import time
from ..items import ReutersItem
from scrapy import Request


def check(arr):
    if type(arr) == 'list':
        return not len(arr) == 0
    return arr is not None


class ReutersSpider(CrawlSpider):
    count = 0
    name = 'reuters'
    # allowed_domains = ['reuters.com']
    start_urls = ['http://www.reuters.com/']
    source = 'reuters'
    crawled_at = int(round(time() * 1000))

    base_url = 'http://www.reuters.com'

    url_tags = {
        '/finance': 'business',
        '/politics': 'politics',
        '/news/technology': 'tech',
        '/commentary': 'commentary',
        '/places/china': 'china',
        '/news/us': 'politics',
        '/news/lifestyle': 'life',
        '/news/entertainment': 'entertainment',
        '/news/entertainment/arts': 'art',
        '/news/sports': 'sport',
        '/news/science':'tech',
        '/commentary': 'commentary'
    }

    def start_requests(self):

        for url, tag in self.url_tags.iteritems():
            if tag == 'china' or tag == 'commentary' or url == '/news/us' or tag == 'art' or url=='/news/science':
                yield scrapy.Request(self.base_url + url, callback=self.parse_zh_list, meta={'tag': tag})
            else:
                yield scrapy.Request(self.base_url + url, callback=self.parse_list, meta={'tag': tag})

    def parse_zh_list(self, res):
        tag = res.meta['tag']
        top_sty = res.xpath('.//div[@class="topStory"]')

        top_sty_url = top_sty.xpath(
            './/div[@class="photo"]/a/@href').extract_first()
        yield Request(self.base_url + top_sty_url, callback=self.parse_art, meta={'tag': tag})

        more_ = res.xpath('.//div[@id="moreSectionNews"]')

        more_urls = more_.xpath(
            './/div[@class="moduleBody"]//div[@class="feature"]/h2/a/@href').extract()

        for url in more_urls:
            yield Request(self.base_url, callback=self.parse_art, meta={'tag': tag})

    def parse_list(self, res):

        tag = res.meta['tag']
        main_panel = res.css('.column1.gridPanel.grid8')
        if not check(main_panel):
            raise Exception('main pannel not found!')
        top_sty = main_panel.xpath('.//div[@id="topStory"]')

        top_sty_url = top_sty.xpath(
            './/div[@class="photo"]/a/@href').extract_first()
        yield Request(self.base_url + top_sty_url, callback=self.parse_art, meta={'tag': tag})

        right = main_panel.xpath('.//div[@class="columnRight"]')

        r_urls = right[0].xpath(
            './/div[@class="moduleBody"]/ul/li/a/@href').extract()

        for url in r_urls:
            yield Request(self.base_url + url, callback=self.parse_art, meta={'tag': tag})

        more_ = res.xpath('.//div[@id="moreSectionNews"]')

        more_urls = more_.xpath(
            './/div[@class="moduleBody"]//div[@class="feature"]/h2/a/@href').extract()

        for url in more_urls:
            print('common', url)
            yield Request(self.base_url, callback=self.parse_art, meta={'tag': tag})

        left = res.xpath('.//div[@class="columnLeft"]')
        if len(left) > 1:
            l = left[1]
            ul = l.xpath('.//h2/a/@href').extract_first()
            yield Request(self.base_url + ul, callback=self.parse_art, meta={'tag': tag})

        if len(right) > 1:
            r = right[1]
            ul = l.xpath('.//h2/a/@href').extract_first()
            yield Request(self.base_url + ul, callback=self.parse_art, meta={'tag': tag})

    def parse_art(self, res):
        self.count += 1
        print(self.count)
