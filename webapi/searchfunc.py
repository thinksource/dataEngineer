import pymongo
from flask import jsonify
from config import collection


def list_by_keywords(keyword, page, perpage):
    skip = (page - 1) * perpage    
    resultlist=collection.find({"keywords":keyword.capitalize()}).skip(skip).limit(perpage)
    ret = []
    for i in resultlist:
        tmp = {}
        tmp['headline'] = i['headline']
        tmp['keywords'] = i['keywords']
        tmp['description'] = i['description']
        tmp['url'] = i['url']
        tmp['sha1'] = i['sha1']
        tmp['viewtime'] = i['viewtime']
        ret.append(tmp)
    return jsonify(ret)

def show_details(sha1):
    result = collection.find_one({"sha1": sha1})
    return jsonify(result)