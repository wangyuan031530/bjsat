# -*- coding: utf-8 -*-
import scrapy,json, requests,demjson
from jsonpath import jsonpath
from bjsat.items import FeizhengItem
from datetime import datetime

class FeizhengSpider(scrapy.Spider):
    name = 'feizheng'
    allowed_domains = ['www.bjsat.gov.cn']
    pageNo = 1
    pageSize = 10
    page_size = 1000
    url = 'http://www.bjsat.gov.cn/WSBST//FZCHGL_FYServlet'
    headers={
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "www.bjsat.gov.cn",
        "Origin": "http://www.bjsat.gov.cn",
        "Referer": "http://www.bjsat.gov.cn/WSBST/qd/fzchgl/jsp/ggnr.jsp",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    def start_requests(self):

        url = 'http://www.bjsat.gov.cn/WSBST/qd/fzchgl/jsp/ggnr.jsp'

        yield scrapy.Request(url=url, callback=self.parse, headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "www.bjsat.gov.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
        })

    def parse(self, response):

        code_list = response.xpath('//*[@id="select2"]/option[position()>1]/@value').extract()

        for code in code_list:

            result = requests.post(self.url, data={"qxfj":code , "nsrsbh":"", "nsrmc":"", "pageNo":str(self.pageNo), "pageSize":str(self.pageSize)}, headers=self.headers).text

            #jsonobj = json.loads(result.text, strict=False)
            jsonobj = demjson.decode(result.text)

            totalNum = int(jsonpath(jsonobj, '$..totalNum')[0])

            if totalNum % self.pageSize == 0:

                pagesNum = totalNum // self.page_size

            else:

                pagesNum = totalNum // self.page_size + 1

            yield scrapy.FormRequest(url=self.url, formdata={"qxfj":code , "nsrsbh":"", "nsrmc":"", "pageNo":str(i for i in range(1,pagesNum)), "pageSize":str(self.pageSize)}, headers=self.headers, callback=self.parse_item)

    def parse_item(self,response):
        #jsonobj = json.loads(response.text)
        jsonobj = demjson.decode(response.text)

        data_list = jsonpath(jsonobj, '$..arrayList')[0]

        for data in data_list:

            item = FeizhengItem()

            item['taxpayer_type'] = data['NSRLX']

            item['company'] = data['MC']

            item['identity_num'] = data['NSRSBH']

            item['taxpayer_state'] = data['NSRZT']

            item['name'] = data['XM']

            item['card_id'] = data['ZJHM']

            item['address'] = data['JYDD']

            item['sslong'] = data['RDRQ']

            item['publish_time'] = data['GXRQ']

            item['publish_org'] = data['SWJGMC'] + '国家税务局'

            item['spider_time'] = datetime.now()

            yield item





