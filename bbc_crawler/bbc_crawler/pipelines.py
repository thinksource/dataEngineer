# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
import logging
from scrapy.conf import settings
import pymongo

class BbcCrawlerPipeline(object):

    def __init__(self):
        client = pymongo.MongoClient(dbstr)
        self.post = client['news']
        

    
    def process_item(self, item, spider):
        logging.info(str(item))
        
            self.post.insert(dict(item))
        input()
        return item
