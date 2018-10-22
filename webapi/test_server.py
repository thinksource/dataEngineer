import os

import pytest
import json
from config import app, collection
import logging
import hashlib
sha1 = hashlib.sha1()
testitem1 = {
    "headline": "How one man took on Wall Street and won",
    "author": "https://www.facebook.com/bbcnews",
    "keywords": ["Entrepreneurship", "Stock markets"],
    "description": "A profile of stockbroker Brad Katsuyama, who devised a way to prevent the controversial practice of high frequency trading on the US financial markets.",
    "text": "test message",
    "viewtime": "2018-10-22 01:10:40",
    "url": "https://www.bbc.com/news/business-36544970"
    }
testitem2 = {
    "headline": "How one man took on Wall Street and won",
    "author": "https://www.facebook.com/bbcnews",
    "keywords": ["Entrepreneurship", "Stock markets"],
    "description": "A profile of stockbroker Brad Katsuyama, who devised a way to prevent the controversial practice of high frequency trading on the US financial markets.",
    "text": "test another message",
    "viewtime": "2018-10-22 01:10:40",
    "url": "https://www.bbc.com/news/business-test"
    }

@pytest.fixture
def client():
    # collection=json.load(open("..\\testdb.json"))
    client= app.test_client()
    yield client


def test_news(client):
    sha1.update(testitem1['text'].encode('utf-8'))
    testitem1['sha1'] = str(sha1.hexdigest())
    collection.insert_one(dict(testitem1))
    sha1.update(testitem2['text'].encode('utf-8'))
    testitem2['sha1'] = str(sha1.hexdigest())
    collection.insert_one(dict(testitem2))
    rs = client.get('/api/news?keyword=Entrepreneurship&page=1&perpage=2')
    logging.info(rs.data)
    collection.delete_one({'sha1': testitem1['sha1']})
    collection.delete_one({'sha1': testitem2['sha1']})
    assert 200 == rs.status_code
    rsjson = json.loads(rs.data)
    assert 2 == len(rsjson)
    assert 'sha1' in rsjson[0]
    assert 'keywords' in rsjson[0]
    assert 'headline' in rsjson[0]
    assert 'url' in rsjson[0]
    

def test_news_sha1(client):
    sha1.update(testitem1['text'].encode('utf-8'))
    testitem1['sha1'] = str(sha1.hexdigest())
    collection.insert_one(dict(testitem1))
    rs = client.get('/api/news/{}'.format(sha1.hexdigest()))
    collection.delete_one({'sha1': sha1.hexdigest()})
    assert 200 == rs.status_code
    rsjson = json.loads(rs.data)
    assert 'sha1' in rsjson
    assert 'keywords' in rsjson
    assert 'headline' in rsjson
    assert 'url' in rsjson
    assert testitem1["text"] == rsjson['text']
    assert testitem1['url']==rsjson['url']