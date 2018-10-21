# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
import logging
from scrapy.conf import settings
import pymongo
from pymongo import IndexModel

dbstr='mongodb+srv://admin:mongo123@cluster0-hngx9.mongodb.net/crawlerdb'
index_name="search_index"
class BbcCrawlerPipeline(object):

    def __init__(self):
        index_keywords = IndexModel([('keywords', pymongo.TEXT)], name=index_name, default_language='english')
        index_sha1=IndexModel([('sha1', pymongo.ASCENDING)], name="index_sha1")
        client = pymongo.MongoClient(dbstr)
        self.collection = client['crawlerdb']['news']
        if not index_name in self.collection.index_information():
            self.collection.create_indexes([index_keywords])
        if not "index_sha1" in self.collection.index_information():
            self.collection.create_indexes([index_sha1])
    
    def process_item(self, item, spider):
        # logging.info(str(item))
        valid = True
        for data in item:
            if not data:
                valid = False
                logging.warn("Missing {}!".format(data))
            if self.collection.find_one({"sha1": item["sha1"]}):
                valid = False
                logging.warn("url: {} already exist".format(item["url"]))
        if valid:
            self.collection.insert(dict(item))
            logging.info("url: {0} data added to database!".format(item['url']))
            return item
