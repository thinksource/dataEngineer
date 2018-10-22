
# README



Create **collection** news on **crawlerdb** database on MongoDB.

You need to install requirements in requirement.txt before you run it.



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

1. there is lots of articles in bbc.com do not have author, so it will be "https://www.facebook.com/bbcnews" in the author.

2. I use **xpath** filter to clean the  superfluous content

```
"*[not(descendant-or-self::style |descendant-or-self::iframe | descendant-or-self::figure | descendant-or-self::script | descendant-or-self::div[contains(@class, 'bbccom_advert')] | descendant-or-self::div[contains(@class, 'teads-inread')] | descendant-or-self::div[contains(@class, 'twitter-wrap')])]"
```
Those content including javascript, css, iframe, figure and bbccom advertiement, google advertisement(class is teads-inread) and twiter ad, which is class(twitter-wrap).

There may have another ads, I may not cleanup.

3. The keywords is base on Related Topics, if there is no Related Topic, there will be empty keywords.

4. Spider do not duplicate grab pages depending on two things:

4.1. Spider rule have LinkExtractor setting unique=True

4.2. the sha1 is additional index of article, if the sha1 string is equal, even if the url is different it still can not insert into the database, according to valid variable.



## Search api

the search string is **case sensetive**. The default word use captitalize() function as keyword.

fellowing the OpenAPI 2.0, **swagger 2.0** rules.

get:

http://localhost:5000/api/news/{sha1}

This way will display all contents of article.


get:

http://localhost:5000/api/news?keyword=keywords&page=1&perpage=20

The list api do not show the content(text part) of article.

### swagger ui:

http://localhost:5000/api/ui/#/Search


## command line:

The running server commandline in webapi/manage.py

you can run it base like:

```
python manage.py runserver
```



## testing

Just testing the rest APIs, it is really hard to test Spider.