# -*- coding: utf-8 -*-

import scrapy
import json
import re


from testScrapy.yidianzixun.yidian.settings import BASE_DIR
from urllib.parse import urlencode
from datetime import datetime
from testScrapy.yidianzixun.yidian.items import YidianItem

class YidianSpider(scrapy.Spider):
    name = 'yidian'
    allowed_domains = ['yidianzixun.com']

    start_url = 'http://www.yidianzixun.com/channel/u8339'

    cstart = 0
    cend = 10
    page_list = []
    while cstart <= 40:
        page_list_one = []
        page_list_one.append(cstart)
        page_list_one.append(cend)
        page_list.append(page_list_one)
        cstart += 10
        cend += 10

    new_list = ['u8839', 'sc43', 'v33616', 'sc44', 'u75', 'u9608', 't1111', 'sc38', 'c3', 's10671', 'u8343']
    yingping_url_list = []

    for news in new_list:
        for page in page_list:
            yingping_url = 'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=' + news + '&cstart=' + str(page[0]) + '&cend=' + str(page[1])
            yingping_url_list.append(yingping_url)


    def parse_sptoken(self,sptoken):
        if isinstance(sptoken,str):
            temp_sptoken = ''
            for s in sptoken:
                s = 10 ^ ord(s)
                temp_sptoken += chr(s)
            return urlencode({'sptoken':temp_sptoken}).split('=')[1]


    def parse_day(self, days):
        if isinstance(days, str):
            later = datetime.strptime(days, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            delta = now - later
            if not delta.days:
                return int((delta.seconds)/3600)
        else:
            return None

    def start_requests(self):
        print("----start_request-----")
        yield scrapy.Request(
            self.start_url,
            callback = self.parse_id,
            cookies = {}
        )

    def parse_id(self, response):
        print("----parse_id-----")
        cookie_list =response.headers.getlist('Set-Cookie')[0].decode().split(";")[0].split("=")


        for url in self.yingping_url_list:
            cookie = {}
            u = re.compile("channel_id=(.*)&cstart=(.*)&cend=(.*)").findall(url)
            sptoken = '_' + '_'.join(list(u[0])) + '_'
            cookie[cookie_list[0]] = self.parse_sptoken(sptoken) + cookie_list[1]
            request = scrapy.Request(
                url,
                cookies=cookie,
                # meta={'dont_merge_cookies': True},
                callback=self.parse_html,
                dont_filter=True
            )
            yield request


    def parse_html(self, response):
        print("---parse_html---")
        new_dict = json.loads(response.body.decode())

        result_list = new_dict.get('result', None)

        if result_list:
            for news_dict in result_list:
                hours = self.parse_day(news_dict.get('date',None))
                count = int(news_dict.get('comment_count',0))

                if (hours != None) and count:
                    if hours <= 2 and count >= 3:
                        print('-----item-----')
                        yidian_item = YidianItem()
                        yidian_item['title'] = news_dict.get('title', None).replace("?", ",").replace("“", "")
                        yidian_item['hours'] = hours
                        yidian_item['comment_count'] = count
                        yidian_item['category'] = news_dict.get('category', None)
                        yidian_item['ctype'] = news_dict.get('ctype', None)
                        yidian_item['url'] = "http://www.yidianzixun.com/article/" + news_dict.get('docid', '')
                        yield yidian_item