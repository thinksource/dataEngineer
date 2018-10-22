
# README
create collection craw

## database setting

the database connection is store in db.txt, which is not loaded on github. you should use your own database connection string.


## RUN spider

```
scrapy crawl BBCspider -o spider.json
```

## Search api

the search string is case sensetive. The default use captitalize() string as keyword.

