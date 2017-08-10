# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from stacklib.item import CNNItem as CNN
from time import time
from scrapy.loader import ItemLoader
from scrapy import Request

# image not accurate


def checkUrl(urls):
    if urls is None:
        return urls

    return [url for url in urls if not (url.startswith('http') or url.startswith('https'))]


class CnnSpider(CrawlSpider):
    source = 'cnn'
    crawled_at = int(round(time() * 1000))
    count = 0

    name = 'cnn'
    # allowed_domains = ['edition.cnn.com']
    start_urls = ['http://edition.cnn.com', 'http://money.cnn.com']
    base_url = start_urls[0]

    url_tags = {
        '/INTERNATIONAL': 'business',
        '/entertainment': 'entertainment',
        '/asia': 'world',
        '/china': 'china',
        '/us': 'world',
        '/technology': 'tech',
        '/sport': 'sport',
        '/travel': 'travel',
        '/health': 'health',
    }

    def busi_list(self, res):

        tag = res.meta['tag']
        urls = res.xpath(
            './/a[re:test(@href,"^/\d{4}/\d{2}/\d{2}/.*$")]/@href').extract()
        for url in urls:
            yield Request("http://money.cnn.com" + url, callback=self.parse_busi_art, meta={'tag': tag})

        urls_ = res.xpath(
            './/a[re:test(@href,"^http://money.cnn.com/\d{4}/\d{2}/\d{2}/.*$")]/@href').extract()

        for url in urls_:
            yield Request(url, callback=self.parse_busi_art, meta={'tag': tag})

    def parse_busi_art(self, res):
        tag = res.meta['tag']

        url = res.url
        main = res.css('.container.js-social-anchor-start')
        ci = ItemLoader(item=CNN(), selector=main)

        ci.add_value('tag', tag)
        ci.add_value('crawled_at', self.crawled_at)
        ci.add_value('url', url)

        ci.add_css('title', 'h1.article-title.speakable::text')

        ci.add_xpath('timestamp', './/span[@class="cnnDateStamp"]/text()')

        img_ = main.xpath('.//div[@id="storytext"]//img/@src').extract()

        ci.add_value('image_urls', img_)
        ci.add_css('summary', 'h2.speakable::text')

        ci.add_xpath('text', './/p/text()')
        ci.add_value('source', self.source)

        return ci.load_item()

        # self.count+=1

    def ent_list(self, res):
        tag = res.meta['tag']
        urls = res.xpath(
            './/a[re:test(@href,"^/\d{4}/\d{2}/\d{2}/.*$")]/@href').extract()
        if not (len(urls) == 0):
            for url in urls:
                yield Request(self.base_url + url, callback=self.parse_ent_art, meta={'tag': tag})

    def parse_ent_art(self, res):
        '''
        entertainment,china,asia,sport,health,us
        '''

        # http://edition.cnn.com/2017/08/08/entertainment/taylor-swift-lawsuit-court-rules/index.html
        url = res.url
        tag = res.meta['tag']
        art = res.xpath(
            './/div[@class="l-container"][descendant::div[@class="pg-rail-tall__wrapper"]]')
        ci = ItemLoader(item=CNN(), selector=art)

        ci.add_value('crawled_at', self.crawled_at)
        ci.add_value('tag', tag)
        ci.add_value('url', url)
        ci.add_value('source', self.source)

        summary = ' '.join(art.xpath(
            './/div[@class="el__storyhighlights_wrapper"]//ul/li/text()').extract())
        ci.add_value('summary', summary)

        ci.add_xpath('title', './/h1[@class="pg-headline"]/text()')
        ci.add_xpath(
            'timestamp', './/div[@class="metadata"]//p[@class="update-time"]/text()')

        # ci.add_xpath('text','.//div[@class="pg-rail-tall__body"]//div[@class="el__leafmedia el__leafmedia--sourced-paragraph"]|div[@class="el__leafmedia el__leafmedia--sourced-paragraph"]|div[@class=""]')
        ci.add_css('text', '.zn-body__paragraph')

        ci.add_xpath('image_urls',   './/img/@data-src-medium')

        return ci.load_item()

    def asia_list(self, res):
        tag = res.meta['tag']
        urls = res.xpath(
            './/a[re:test(@href,"^/\d{4}/\d{2}/\d{2}/.*$")]/@href').extract()
        if not (len(urls) == 0):
            for url in urls:
                yield Request(self.base_url + url, callback=self.parse_ent_art, meta={'tag': tag})

    def china_list(self, res):
        tag = res.meta['tag']
        urls = res.xpath(
            './/a[re:test(@href,"^/\d{4}/\d{2}/\d{2}/.*$")]/@href').extract()
        if not (len(urls) == 0):
            for url in urls:
                yield Request(self.base_url + url, callback=self.parse_ent_art, meta={'tag': tag})

    def us_list(self, res):
        tag = res.meta['tag']
        urls = res.xpath(
            './/a[re:test(@href,"^/\d{4}/\d{2}/\d{2}/.*$")]/@href').extract()
        if not (len(urls) == 0):
            for url in urls:
                yield Request(self.base_url + url, callback=self.parse_ent_art, meta={'tag': tag})

    def tech_list(self, res):
        tag = res.meta['tag']
        urls = res.xpath(
            './/a[re:test(@href,"^//money.cnn.com/\d{4}/\d{2}/\d{2}/technology/.*$")]/@href').extract()
        if not (len(urls) == 0):
            for url in urls:
                yield Request("http:" + url, callback=self.parse_busi_art, meta={'tag': tag})

    def sport_list(self, res):
        tag = res.meta['tag']
        urls = res.xpath(
            './/a[re:test(@href,"^/\d{4}/\d{2}/\d{2}/.*$")]/@href').extract()
        if not (len(urls) == 0):
            for url in urls:
                yield Request(self.base_url + url, callback=self.parse_ent_art, meta={'tag': tag})

    def travel_list(self, res):
        urls = res.xpath(
            './/a[re:test(@href,"^/travel/article/.*$")]/@href'

        ).extract()

        for url in urls:
            yield Request(url=self.base_url + url, callback=self.parse_travel_art, meta={'tag': res.meta['tag']})


    def parse_travel_art(self, res):
        # http://edition.cnn.com/travel/article/singlethread-restaurant-sonoma-county-california/index.html

        url = res.url
        tag = res.meta['tag']

        art = res.xpath('.//div[@class="Article__wrapper"]')

        ci = ItemLoader(CNN(), selector=art)
        ci.add_value('url', url)
        ci.add_value('crawled_at', self.crawled_at)
        ci.add_value('tag', tag)
        ci.add_value('source', self.source)

        ci.add_xpath('title', './/h1[@class="Article__title"]/text()')

        ci.add_xpath('timestamp', './/div[@class="Article__subtitle"]/text()')

        ci.add_xpath('image_urls', './/img/@src')
        ci.add_css('text', '.Paragraph__component')

        return ci.load_item()

    def health_list(self, res):
        tag = res.meta['tag']
        urls = res.xpath(
            './/a[re:test(@href,"^/\d{4}/\d{2}/\d{2}/health/.*$")]/@href').extract()
        # print(urls)
        if not (len(urls) == 0):
            for url in urls:
                yield Request(self.base_url + url, callback=self.parse_ent_art, meta={'tag': tag})

    def start_requests(self):
        base_ = self.base_url
        base_money = self.start_urls[1]

        for url, tag in self.url_tags.iteritems():

            if url == '/china':  # done
                yield Request(base_ + url, callback=self.china_list, meta={'tag': tag})

            if url == '/INTERNATIONAL':  # done
                yield Request(base_money + url, callback=self.busi_list, meta={'tag': tag})

            if url == '/entertainment':  # done

                yield Request(base_ + url, callback=self.ent_list, meta={'tag': tag})
            if url == '/asia':  # done
                yield Request(base_ + url, callback=self.asia_list, meta={'tag': tag})

            if url == '/us':
                yield Request(base_ + url, callback=self.us_list, meta={'tag': tag})

            if url == '/technology':
                yield Request(base_money + url, callback=self.tech_list, meta={'tag': tag})

            if url == '/sport':
                yield Request(base_ + url, callback=self.sport_list, meta={'tag': tag})

            if url == '/travel':  # done todo without image

                yield Request(base_ + url, callback=self.travel_list, meta={'tag': tag})

            if url == '/health':  # done

                yield Request(base_ + url, callback=self.health_list, meta={'tag': tag})
