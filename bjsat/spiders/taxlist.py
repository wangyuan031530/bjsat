# -*- coding: utf-8 -*-
import scrapy, re
from datetime import datetime
from urllib.parse import quote
from bjsat.items import BjsatItem


class TaxlistSpider(scrapy.Spider):
    name = 'taxlist'
    allowed_domains = ['www.bjsat.gov.cn']
    start_url = 'http://www.bjsat.gov.cn/bjsat/office/jsp/qsgg/query.jsp'
    pageNum = 1
    today = datetime.now().strftime("%Y-%m-%d")

    def start_requests(self):

        yield scrapy.Request(url=self.start_url,callback=self.parse)

    def parse(self, response):

        fbdw_list = response.xpath('//select[@name="fbdw"]/option[position()>1]/text()').extract()

        nsrlx_list = response.xpath('//select[@name="nsrlx"]/option[position()>1]/text()').extract()

        for fbdw in fbdw_list:

            for nsrlx in nsrlx_list:

                url_list =[self.start_url + '?fbdw=' + quote(fbdw.strip().encode('GBK')) + '&nsrlx=' + quote(nsrlx.strip().encode('GBK')) + '&BeginTime=2011-01-01&EndTime=' + self.today]

                for url in url_list:

                    yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self,response):

        pattern = re.compile(r'共\d{0,9}页')

        result = pattern.search(response.text).group()

        pages = int(result.split('共')[1].split('页')[0])

        if pages != 0:

            url_list = [response.url + '&page_num=' + str(i) for i in range(1, pages + 1)]

            for url in url_list:

                yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_item(self,response):

        node_list = response.xpath('//form[@name="condition"]/table/tr[1]/td[3]/table[4]/tr[position()>2 and position()<last()]')

        for node in node_list:

            item = BjsatItem()

            item['detail_link'] = response.urljoin(node.xpath('./td[1]/a/@href').extract_first())

            item['publish_org'] = node.xpath('./td[5]/text()').extract_first()

            item['publish_time'] = node.xpath('./td[6]/text()').extract_first()

            yield scrapy.Request(item['detail_link'], meta = {"item" : item}, callback=self.parse_content)

    def parse_content(self, response):

        item = response.meta['item']

        item['new_tax_amount'] = response.xpath('//*[@class="table_04"]/tr/td/table/tr[9]/td[2]/text()').extract_first()

        item['tax_amount'] = response.xpath('//*[@class="table_04"]/tr/td/table/tr[8]/td[2]/text()').extract_first()

        item['tax_type'] = response.xpath('//*[@class="table_04"]/tr/td/table/tr[7]/td[2]/text()').extract_first()

        item['address'] = response.xpath('//*[@class="table_04"]/tr/td/table/tr[6]/td[2]/text()').extract_first()

        item['taxpayer_type'] = response.xpath('//*[@class="table_04"]/tr/td/table/tr[2]/td[2]/text()').extract_first()

        item['company'] = response.xpath('//*[@class="table_04"]/tr/td/table/tr[1]/td[2]/text()').extract_first()

        item['identity_num'] = response.xpath('//*[@class="table_04"]/tr/td/table/tr[3]/td[2]/text()').extract_first()

        item['name'] = response.xpath('//*[@class="table_04"]/tr/td/table/tr[4]/td[2]/text()').extract_first()

        item['card_id'] = response.xpath('//*[@class="table_04"]/tr/td/table/tr[5]/td[2]/text()').extract_first()

        item['spider_time'] = datetime.now()


        yield item


