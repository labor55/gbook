# -*- coding: utf-8 -*-
from scrapy.utils.project import get_project_settings
import pymongo


class ScrapyDataPipeline(object):

    config = get_project_settings()

    def __init__(self):
        # 链接数据库
        self.client = pymongo.MongoClient(host=self.config.get('MONGO_HOST'), port=self.config.get('MONGO_PORT'))
        # 获得数据库的句柄
        self.db = self.client[self.config.get('MONGO_DATABASE')]
        # 数据库登录需要帐号密码
        if self.config.get('MONGO_USER') and self.config.get('MONGO_PASSWORD'):
            self.db.authenticate(self.config.get('MONGO_USER'), self.config.get('MONGO_PASSWORD'))
        self.coll = self.db[self.config.get('MONGO_TABLE')]  # 获得collection的句柄

    def process_item(self, item, spider):
        item = dict(item)  # 把item转化成字典形式
        r = self.coll.update(
            {'data_value': item['data_value'], 'create_time': item['create_time'], 'parent_id': item['parent_id'],
             'frequency': item['frequency']}, {'$setOnInsert': item}, True)
        return item

    def close_spider(self, spider):
       self.client.close()


class ScrapyInfoPipeline(object):
    config = get_project_settings()

    def __init__(self):
        # 链接数据库
        self.client = pymongo.MongoClient(host=self.config.get('MONGO_HOST'), port=self.config.get('MONGO_PORT'))
        self.db = self.client[self.config.get('MONGO_DATABASE')]
        if self.config.get('MONGO_USER') and self.config.get('MONGO_PASSWORD'):
            self.db.authenticate(self.config.get('MONGO_USER'), self.config.get('MONGO_PASSWORD'))
        self.coll = self.db[self.config.get('MONGO_TABLE')]

    def process_item(self, item, spider):
        item = dict(item)  # 把item转化成字典形式
        self.coll.update({'news_id': item['news_id']}, {'$setOnInsert': item}, True)  # 符合条件的数据存在则不执行插入
        return item

    def close_spider(self, spider):
        self.client.close()


class ScrapyReportPipeline(object):
    config = get_project_settings()

    def __init__(self):
        # 链接数据库
        self.client = pymongo.MongoClient(host=self.config.get('MONGO_HOST'), port=self.config.get('MONGO_PORT'))
        self.db = self.client[self.config.get('MONGO_DATABASE')]
        if self.config.get('MONGO_USER') and self.config.get('MONGO_PASSWORD'):
            self.db.authenticate(self.config.get('MONGO_USER'), self.config.get('MONGO_PASSWORD'))
        self.coll = self.db[self.config.get('MONGO_TABLE')]

    def close_spider(self, spider):
        """
        爬虫一旦关闭，就会实现这个方法，关闭数据库连接
        """
        self.client.close()

    def process_item(self, item, spider):
        """
        每个实现保存的类里面必须都要有这个方法，且名字固定，用来具体实现怎么保存
        """
        self.db[self.collection_name].update({'paper_url': item['paper_url']}, {'$setOnInsert': item}, True)
        return item
