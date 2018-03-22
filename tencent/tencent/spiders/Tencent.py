# -*- coding: utf-8 -*-
import scrapy
from re import findall
from tencent.items import TencentItem

def judge(item, attr_name, string):
    if string:
        item[attr_name] = string[0]
    else:
        item[attr_name] = '无'


class TencentSpider(scrapy.Spider):
    name = 'Tencent'
    allowed_domains = ['tencent.com']

    url = 'https://hr.tencent.com/position.php?&start='
    min_index = 0
    max_index = 0
    # 执行一次获取最后页码
    flag = True
    start_urls = [url+str(min_index)]

    def parse(self, response):
        # 爬取一页数据
        for each in  response.xpath("//tr[@class='even'] | //tr[@class='odd']"):
            print(each)
            item = TencentItem()
            # 职位名称
            item['position_name'] = each.xpath("./td[1]/a/text()").extract()[0]
            # 职位链接
            item['position_link'] = each.xpath("./td[1]/a/@href").extract()[0]
            # 职位类别
            judge(item,'position_type', each.xpath("./td[2]/text()").extract())
            # item['position_type'] = each.xpath("./td[2]/text()").extract()[0]
            # 职位人数
            item['position_people'] = each.xpath("./td[3]/text()").extract()[0]
            # 职位地址
            item['position_add'] = each.xpath("./td[4]/text()").extract()[0]
            # 发布时间
            item['position_time'] = each.xpath("./td[5]/text()").extract()[0]
            # 返回数据item给pipelines.py管道文件
            yield item
        # 执行一次获取最后一页页码
        if self.flag:
            self.max_index = response.xpath("//div[@class='pagenav']/a[10]/@href").extract()[0]
            self.max_index = findall("\d+",self.max_index)[0]
            self.max_index = int(self.max_index)
            print(self.max_index)
            self.flag = False
        if self.min_index < self.max_index:
            self.min_index += 10
        # 重复请求自动退出
        yield scrapy.Request(self.url+str(self.min_index),callback=self.parse)
        print(self.max_index)