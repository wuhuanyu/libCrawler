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
        if 'text' not in item.keys():
            return item
        if 'source' not in item.keys():
            raise Exception('No source field in item')
        self.__get_collection(item['source']).insert_one(dict(item))
        return item
