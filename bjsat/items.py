# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BjsatItem(scrapy.Item):
    # define the fields for your item here like:

    #详情链接
    detail_link = scrapy.Field()
    #发布单位
    publish_org = scrapy.Field()
    #发布时间
    publish_time = scrapy.Field()
    # 公司名称
    company = scrapy.Field()
    # 纳税人类型
    taxpayer_type = scrapy.Field()
    # 纳税人识别号
    identity_num = scrapy.Field()
    # 负责人姓名
    name = scrapy.Field()
    # 证件号码
    card_id = scrapy.Field()
    # 经营地点
    address = scrapy.Field()
    # 欠税税种
    tax_type = scrapy.Field()
    # 欠税余额
    tax_amount = scrapy.Field()
    # 当前新发生的欠税余额
    new_tax_amount = scrapy.Field()
    # 爬取时间
    spider_time = scrapy.Field()


class FeizhengItem(scrapy.Item):
    #纳税人类型
    taxpayer_type = scrapy.Field()
    #企业或单位名称(个体工商户为业户名称)
    company = scrapy.Field()
    #纳税人识别号
    identity_num = scrapy.Field()
    #纳税人状态
    taxpayer_state = scrapy.Field()
    #法定代表人或负责人姓名(个体工商户为业主姓名)
    name = scrapy.Field()
    #居民身份证或其他有效身份证件号码
    card_id = scrapy.Field()
    #经营地点
    address = scrapy.Field()
    #认定非正常户日期
    sslong = scrapy.Field()
    #数据更新日期
    publish_time = scrapy.Field()
    #发布机构
    publish_org = scrapy.Field()
    #爬取时间
    spider_time = scrapy.Field()




