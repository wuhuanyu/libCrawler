# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from time import time
from scrapy import Request

from stacklib.item.NewsItem import ReutersItem


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
        '/places/china': 'china',
        '/finance': 'business',
        '/politics': 'politics',
        '/news/technology': 'tech',
        '/commentary': 'commentary',
        '/news/us': 'politics',
        '/news/lifestyle': 'life',
        '/news/entertainment': 'entertainment',
        '/news/entertainment/arts': 'art',
        '/news/sports': 'sport',
        '/news/science': 'tech',
    }

    def start_requests(self):

        for url, tag in self.url_tags.iteritems():
            if tag == 'china' or tag == 'commentary' or url == '/news/us' or tag == 'art' or url == '/news/science':
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
        tag = res.meta['tag']
        url = res.url
        main = res.xpath('.//div[@class="ArticlePage_container_2aGp_"]')
        if not check(main):
            raise Exception('NO main body found')

        rl = ItemLoader(item=ReutersItem(), selector=main)
        rl.add_value('crawled_at', self.crawled_at)
        rl.add_value('tag', tag)
        rl.add_value('url', url)
        rl.add_value('source', self.source)

        rl.add_xpath(
            'timestamp', './/div[re:test(@class,"ArticleHeader_date.*")]/text()')
        image_url = main.xpath(
            './/div[re:test(@class,"LazyImage_container.*")]/img/@src').extract_first()
        if image_url is not None:
            image_url += '&w=300'

            rl.add_value('image_urls', [image_url, ])

        rl.add_xpath(
            'title', './/h1[re:test(@class,"ArticleHeader_headline.*")]/text()')

        rl.add_xpath(
            'text', './/div[re:test(@class,"ArticleBody_body.*")]/p/text()')

        return rl.load_item()
