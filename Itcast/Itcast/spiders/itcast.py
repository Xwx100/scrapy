# -*- coding: utf-8 -*-
import scrapy
from Itcast.items import ItcastItem


class ItcastSpider(scrapy.Spider):
    name = "itcast"
    allowed_domains = ["itcast.cn",]
    start_urls = ["http://www.itcast.cn/channel/teacher.shtml",]

    def parse(self, response):
        # pass
        # items不交给管道处理
        # items = []

        print("-"*30)
        # xpath返回的都是列表
        # extract把xpath对象转化为Unicode
        for each in response.xpath("//div[@class='li_txt']"):
            # 生成item类似字典
            item = ItcastItem()
            item['name'] = each.xpath("h3/text()").extract()[0]
            item['level'] = each.xpath("h4/text()").extract()[0]
            item['info'] = each.xpath("p/text()").extract()[0]
            # 直接把字典返回给管道进行处理
            yield item
            # items.append(item)
        #  不交给管道进行处理，直接返回所需数据
        # return items

