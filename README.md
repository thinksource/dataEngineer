
# README
create collection craw

## database setting

the database connection is store in **db.txt**, which is not loaded on github. you should use your own database connection string replace these part.


## RUN spider

go to bbc_crawler directory
```
scrapy crawl BBCspider 
```

The spider speed is in settings.py:

```
ITEM_PIPELINES = {
   'bbc_crawler.pipelines.BbcCrawlerPipeline': 300,
}
```

## pipeline:

the pipeline is first get element into item and using BbcCrawlerPipeline to store the string into mongodb database.

## Spider special:

1. there is lots of passage in bbc.com do not have author, so it will be "https://www.facebook.com/bbcnews"

2. I use **xpath** filter to clean the  superfluous content

```
"*[not(descendant-or-self::style |descendant-or-self::iframe | descendant-or-self::figure | descendant-or-self::script | descendant-or-self::div[contains(@class, 'bbccom_advert')] | descendant-or-self::div[contains(@class, 'teads-inread')] | descendant-or-self::div[contains(@class, 'twitter-wrap')])]"
```
Those content including javascript, css, iframe, figure and bbccom advertiement, google advertisement(class is teads-inread) and twiter ad, which is class(twitter-wrap).

There may have another ads, I may not cleanup.


## Search api

the search string is case sensetive. The default use captitalize() string as keyword.




### swagger ui:

http://localhost:5000/api/ui/#/Search


## testing

Just using the pip