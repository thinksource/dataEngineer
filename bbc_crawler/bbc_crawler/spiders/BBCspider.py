# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Request
from bbc_crawler.items import BbcCrawlerItem
from datetime import datetime
import logging
import re
class BbcspiderSpider(CrawlSpider):
    name = 'BBCspider'
    allowed_domains = ['www.bbc.com']
    start_urls = ['http://www.bbc.com/news','https://www.bbc.com/news/stories']

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
            body_sc = response.xpath("//div[@class='story-body__inner']")[0]
            text = body_sc.xpath("string(.)").extract_first()
            item['text']=re.sub(r'[ ]+\n', '', text)
            
            item["viewtime"] = datetime.utcnow()
            item["url"] = response.url

            # text.replace('\n', '') 
            
            yield item
