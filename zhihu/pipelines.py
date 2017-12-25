# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from selenium import webdriver

from pymongo import MongoClient

# config
ip = ""
database = ""
collection = ""
user = ""
pwd = ""

class ZhihuPipeline(object):

    def __init__(self):
        print("init mongo")
        self.client = MongoClient(ip)
        self.db = self.client[database]
        self.db.authenticate(user, pwd)
        self.collection = self.db[collection]

    def process_item(self, item, spider):
        image_url = item["url"]
        self.collection.update_one({"url": image_url}, {"$set": item}, upsert=True)
        return item

    def close_spider(self, spider):
        print("close mongodb")
        self.client.close()
        pass


if __name__ == '__main__':
    url = "https://www.zhihu.com/signin"
    if "signin" in url:
        print("true")
    else:
        print("false")
    # drive = webdriver.Chrome()
    # drive.get("https://www.zhihu.com/#signin")
