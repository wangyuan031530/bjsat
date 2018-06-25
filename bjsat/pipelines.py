# -*- coding: utf-8 -*-
from bjsat.items import BjsatItem
from bjsat.items import FeizhengItem
from twisted.enterprise import adbapi
import scrapy, pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BjsatPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(host='10.3.1.3', port=3306, user='root', password='moerlong', db='spider_data', charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        if isinstance(item, BjsatItem):

            insert_sql = 'insert into taxlist(detail_link, company, identity_num, name, card_id, publish_org, publish_time, spider_time, address, taxpayer_type, tax_type, tax_amount, new_tax_amount) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

            params = [item['detail_link'], item['company'], item['identity_num'], item['name'],
                      item['card_id'], item['publish_org'], item['publish_time'], item['spider_time'],
                      item['address'], item['taxpayer_type'],  item['tax_type'], item['tax_amount'], item['new_tax_amount']]

            self.cursor.execute(insert_sql, params)

            self.conn.commit()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()


class BjsatFeiZhengPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(host='10.3.1.3', port=3306, user='root', password='moerlong', db='spider_data', charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        if isinstance(item, FeizhengItem):

            insert_sql = 'insert into fei_zheng(taxpayer_type, company, identity_num, status, name, card_id, company_addr, sslong, publish_org, publish_time, spider_time) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

            params = [item['taxpayer_type'], item['company'],item['identity_num'], item['taxpayer_state'], item['name'],
                      item['card_id'],item['address'],item['sslong'],item['publish_org'],item['publish_time'],item['spider_time']]

            self.cursor.execute(insert_sql, params)

            self.conn.commit()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

# class BjsatFeiZhengPipeline(object):
#
#     def __init__(self,host,user,password,db):
#         params=dict(
#             host = '139.199.111.244',
#             user = 'root',
#             password = '111',
#             db = 'black_list',
#             charset = 'utf8',
#             cursorclass = pymysql.cursors.DictCursor
#         )
#         # 使用Twisted中的adbapi获取数据库连接池对象
#         self.dbpool=adbapi.ConnectionPool('pymysql',**params)
#
#     @classmethod
#     def from_crawler(cls,crawler):
#         # 获取settings文件中的配置
#         host=crawler.settings.get('HOST')
#         user=crawler.settings.get('USER')
#         password=crawler.settings.get('PASSWORD')
#         db=crawler.settings.get('DB')
#         return cls(host,user,password,db)
#
#     def process_item(self,item,spider):
#         # 使用数据库连接池对象进行数据库操作,自动传递cursor对象到第一个参数
#         query=self.dbpool.runInteraction(self.do_insert,item)
#         # 设置出错时的回调方法,自动传递出错消息对象failure到第一个参数
#         query.addErrback(self.on_error,spider)
#         return item
#
#     def do_insert(self,cursor,item):
#         if isinstance(item, FeizhengItem):
#             sql='insert into fei_zheng(taxpayer_type, company, identity_num, status, name, card_id, company_addr, sslong, publish_org, publish_time, spider_time) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
#             args=(item['taxpayer_type'], item['company'],item['identity_num'], item['taxpayer_state'], item['name'],
#                       item['card_id'],item['address'],item['sslong'],item['publish_org'],item['publish_time'],item['spider_time'])
#             cursor.execute(sql,args)
#
#     def on_error(self,failure,spider):
#         spider.logger.error(failure)

