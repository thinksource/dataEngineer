# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Request
from bbc_crawler.items import BbcCrawlerItem
from datetime import datetime
import logging
import re

import hashlib

sha1 = hashlib.sha1()

class BbcspiderSpider(CrawlSpider):
    name = 'BBCspider'
    allowed_domains = ['www.bbc.com']
    start_urls = ['http://www.bbc.com/news',
    'https://www.bbc.com/news/stories'
    # 'https://www.bbc.com/news/world',
    # 'https://www.bbc.com/news/world/africa',
    # 'https://www.bbc.com/news/world/australia',
    # 'https://www.bbc.com/news/world/europe',
    # 'https://www.bbc.com/news/world/latin_america',
    # 'https://www.bbc.com/news/world/middle_east',
    # 'https://www.bbc.com/news/world/us_and_canada',
    # 'https://www.bbc.com/news/world/asia',
    # 'https://www.bbc.com/news/world/asia/china',
    # 'https://www.bbc.com/news/world/asia/india',
    # 'https://www.bbc.com/news/uk',

    ]

    rules = [
        Rule(
            LinkExtractor(allow=r'news', unique=True),
            callback='parse_item', follow=True    
        ),
        Rule(
            LinkExtractor(allow=r'https://traffic.outbrain.com/network', unique=True),
            callback='parse_item', follow=True
        )

    ]
    
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse, dont_filter=True)

    def parse_item(self, response):
        item=BbcCrawlerItem()        
        c_type = response.xpath('//meta[@property="og:type"]/@content').extract_first()
        if (c_type == "article"):
            item['headline'] =response.xpath('//meta[@property="og:title"]/@content').extract_first()
            ar_author = response.xpath('//meta[@property="article:author"]/@content').extract_first()
            author = response.xpath('//meta[@name="author"]/@content').extract_first()
            item["author"]=ar_author if ar_author else author
            item["keywords"] = response.xpath('//div/ul[@class="tags-list"]/li[@class="tags-list__tags"]/a/text()').extract()
            # import pdb; pdb.set_trace()
            item["description"] = response.xpath('//meta[@name="description"]/@content').extract_first()
            body_sc = response.xpath("//div[@class='story-body__inner']")
            if len(body_sc) > 0: 
                text = body_sc[0].xpath("string(.)").extract_first()
            else:
                body_sc = response.xpath("//div[contains(@class,'main_article_text')]")
                text=body_sc[0].xpath("string(.)").extract_first()
            item['text']=re.sub(r'[ ]+\n', '', text)
            
            item["viewtime"] = datetime.utcnow()
            item["url"] = response.url
            sha1.update(item['text'].encode('utf-8'))
            item["sha1"]=str(sha1.hexdigest())
            # text.replace('\n', '') 
            
            yield item
