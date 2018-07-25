# -*- coding: utf-8 -*-
import scrapy
import json
import os

from urllib.parse import urlencode
from testScrapy.yidianzixun.yidian.core.parse_csv import ParseCsv
from testScrapy.yidianzixun.yidian.items import ToutiaoItem
from testScrapy.yidianzixun.yidian.core.article_simillarity import ArticleSimilarity


class ToutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    allowed_domains = ['toutiao.com']
    start_urls = ['http://toutiao.com/']

    def __init__(self, name=None, **kwargs):
        super(ToutiaoSpider,self).__init__(name, **kwargs)
        self.parseCsv = ParseCsv("./html/new.csv")
        self.header_list = self.parseCsv.extract_csv_title()

    def start_requests(self):
        for header in self.header_list:
            search_url = "https://www.toutiao.com/search_content/?offset=0&format=json&count=5&"
            sue = urlencode({'keyword': header})
            search_url += sue
            yield scrapy.Request(
                search_url,
                callback=self.parse_json,
                meta={
                    'filename':header
                },
                dont_filter = True
            )

    def parse_json(self, response):
        print(response.meta['filename'])
        out_dict = json.loads(response.body)
        data_list = out_dict.get('data', None)
        for data_dict in data_list:
            title = data_dict.get('title', None)
            # print(title)
            if title:
                a = ArticleSimilarity()
                percent = a.titleSimilarity(response.meta['filename'], title)
                if  percent >= 50:
                # if percent >= 0:
                    toutiao_item = ToutiaoItem()
                    print(response.meta['filename'])
                    toutiao_item['filename'] = response.meta['filename']
                    toutiao_item['title'] = title
                    toutiao_item['datetime'] = data_dict.get('datetime', '无')
                    toutiao_item['comment_count'] = data_dict.get('comment_count', '无')
                    toutiao_item['media_name'] = data_dict.get('media_name', '无')
                    toutiao_item['percent'] = '%s%%'%percent
                    toutiao_item['article_url'] = "https://www.toutiao.com/a" + data_dict.get('group_id', '无')
                    yield toutiao_item
                else:
                    toutiao_item = ToutiaoItem()
                    print(response.meta['filename'])
                    toutiao_item['filename'] = response.meta['filename']
                    yield toutiao_item

                    """

                    
                    """