# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from iamue_web.items import IamueWebItem

class IamueSpider(scrapy.Spider):
    #设置name
    name = 'iamue'
    #设定域名
    allowed_domains = ['www.iamue.com']
    #填写爬取地址
    start_urls = ['https://www.iamue.com/10000']
    #编写爬取方法
    def parse(self, response):
        if response.status != 404 and response.status != 301 and response.status != 302:
            print(response.status)
            #实例一个容器保存爬取的信息
            item  = IamueWebItem()
            #这部分是爬取部分，使用xpath的方式选择信息，具体方法根据网页结构而定
            #先获取每个div
            content = response.xpath('//div[@class="content"]')
            item['title'] = content.xpath('.//h1[@class="article-title"]/a/text()').extract()[0].strip()
            item['spider_url'] = response.url
            item['image_urls'] = []
            item['content'] = ''
            for p in content.xpath('.//article[@class="article-content"]/p'):
                item['content'] = item['content']+p.extract().strip()
                if p.xpath('.//img/@src').extract():
                    item['image_urls'].append(p.xpath('.//img/@src').extract())
            yield item
        #self.get_next_url(response.url)
        old_url = response.url
        old_id = int(old_url.split('/')[-1])
        new_id = old_id - 1
        if new_id == 0:
            return
        new_url = old_url.replace(str(old_id),str(new_id))
        yield Request(str(new_url), callback=self.parse)