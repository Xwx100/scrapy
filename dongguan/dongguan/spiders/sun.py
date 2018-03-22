# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from dongguan.items import DongguanItem

def judge(fn):
    def issue(list,response):
        # 判断列表是否“有图或有br分段”，存在则“有图或者有br分段”，反而反之
        if '\xa0\xa0\xa0\xa0' in list:
            temp1 = response.xpath("//div[@class='contentext']/text()").extract()
            # 判断是二者情况之一，有值则是有图，无值则是无图
            if temp1:
                return fn(temp1,response)
            else:
                return fn(list,response)

        else:
            return fn(list,response)
    return issue

@judge
def clear_list(list,response):
    # 清除列表，返回字符串，用于简单content
    str = ''
    for s in list:
        str += s
    return str

class SunSpider(CrawlSpider):
    name = 'sun'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/report?page=0']

    page_link = LinkExtractor(allow=r"page=\d+")
    detail_link = LinkExtractor(allow=r"http://wz.sun0769.com/html/question/\d+/\d+.shtml")

    rules = (
        # 页码链接地址需跟进
        Rule(page_link, follow=True),
        # 详细链接地址不跟进，处理元素
        Rule(detail_link, callback="parse_item", follow=False)
    )

    # 解析元素item
    def parse_item(self, response):
        items = DongguanItem()
        temp = response.xpath("//div[@class='pagecenter p3']//strong/text()").extract()
        # 防止空列表，有值列表取列表第一个，空列表取空字符串
        if temp:
            temp = temp[0]
        else:
            temp = ""
        items['title'] = temp.strip().split('\xa0')[0].split('：')[-1]
        items['number'] = temp.strip().split('\xa0')[-1].split(':')[-1]
        items['content'] = clear_list(response.xpath("//div[@class='c1 text14_2']/text()").extract(),response)
        items['url'] = response.url

        yield items
