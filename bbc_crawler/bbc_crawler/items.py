# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BbcCrawlerItem(Item):
    # define the fields for your item here like:
    headline = Field()
    keywords = Field()
    author=Field()
    url = Field()
    text = Field()
    viewtime = Field()
    description = Field()
    sha1=Field()

    

