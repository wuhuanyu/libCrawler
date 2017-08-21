# -*- coding: utf-8 -*-
import scrapy
import hashlib
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from stacklib.item.BookItem import Book as BI
from stacklib.item.BookItem import BookReivew as BR
from stacklib.item.BookItem import Comment as CO

from time import time


from scrapy import Request as Re


class MillionBookSpider(CrawlSpider):
    crawled_at = int(round(time() * 1000))
    name = 'mbook'
    # allowed_domains = ['themillions.com']
    start_urls = ['http://themillions.com']
    source = 'mbook'

    book_sub_url = '/books-reviews'

    rules = (
        Rule(LinkExtractor(allow=r'Items/'),
             callback='parse_item', follow=True),
    )

    def start_requests(self):
        yield Re(url=self.start_urls[0] + self.book_sub_url, callback=self.book_list)

    def book_list(self, res):
        urls = res.css('.bookimages').xpath('.//li/a/@href').extract()

        for url in urls:
            yield Re(url=self.start_urls[0] + url, callback=self.parse_book)

    def parse_book(self, res):
        url = res.url

        main = res.css('#main-content')

        bi = scrapy.loader.ItemLoader(item=BI(), selector=main)
        bi.add_value('source', self.source)
        bi.add_value('crawled_at', self.crawled_at)
        bi.add_value('url', url)

        bi.add_xpath('summary', './/div[@class="article"]//p/text()')
        bi.add_xpath('image_urls', './/div[@id="br-book-detail"]//img/@src')
        title = main.xpath('.//div[@id="br-details"]/h1/a/text()').extract_first().encode('utf-8')

        bi.add_value('title', title)
        bi.add_xpath('author', './/div[@class="br-details"]//h4/text()')

        img_ = main.xpath('.//div[@class="article"]/h2/a/@href').extract()

        related_urls = filter(lambda x: not ('comments' in x), img_)

        bi.add_value('review_urls', related_urls)

        m=hashlib.md5()
        m.update(title)
        book_hash = m.hexdigest()
        bi.add_value('hash_value',book_hash)

        for url in related_urls:
            yield Re(url, callback=self.parse_book_reivew, meta={'book': title,'book_hash':book_hash})

        yield bi.load_item()


# http://www.themillions.com/2013/01/the-testament-of-mary-by-colm-toibin.html
    def parse_book_reivew(self, res):
        book = res.meta['book']
        book_hash= res.meta['book_hash']
        crawled_at = int(round(time()) * 1000)
        source = 'mbookrev'

        art = res.css('#main-content').xpath('./div[@id="article"]')
        cat = art.xpath('./h2/a[@rel]/text()').extract_first()

        if not (cat.lower() == 'reviews'):
            return

        bi = scrapy.loader.ItemLoader(item=BR(), selector=art)
        bi.add_value('crawled_at', crawled_at)
        bi.add_value('source', source)
        bi.add_css('title', 'h2+h3::text')
        bi.add_css('text', '.article-content>p::text')

        bi.add_value('book', book)
        bi.add_value('url', res.url)
        bi.add_value('book_hash',book_hash)

        comments = []

        com_sel = res.css('.commentlist')

        commentli = com_sel.xpath('.//li[re:test(@id,"^comment-\d*$")]')

        for c in commentli:
            comment = CO()
            comment['author'] = c.xpath(
                './/span[@class="author"]/text()').extract_first()

            comment['text'] = c.css('.commenttext>p::text').extract()
            comments.append(comment)

        bi.add_value('comments', comments)

        return bi.load_item()
