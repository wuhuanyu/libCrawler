# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from pymongo import MongoClient


class StacklibPipeline(object):
    def process_item(self, item, spider):
        raise Exception('unimplemted!')


class Persist(StacklibPipeline):
    # def __init__(self, **kw):
        # super.__init__(self, **kw)
    client = MongoClient('localhost', 27017)
    db = client['stacklib']

    def __get_collection(self, source):
        return self.db[source + 's']

    def process_item(self, item, spider):

        if 'source' not in item.keys():
            raise Exception('No source field in item')
        if item['source'] in ['bbc', 'cnn', 'reuters']:
            return self.process_news(item, spider)

        if item['source']=='medium':
            item['summary']=item['text'][1]
        

        self.__get_collection(item['source']).insert_one(dict(item))
        return item

    def process_news(self, item, spider):
        newItem = self.checkNewsItem(item, spider)
        self.__get_collection(item['source']).insert_one(dict(newItem))
        return item

    def checkNewsItem(self, item, spider):
        if 'text' not in item.keys():
            return None

        if 'title' not in item.keys():
            return None
        if 'tag' not in item.keys():
            raise Exception('No tag check code')
        if 'summary' not in item.keys():
            item['summary'] = item['text'][0]
        return item
