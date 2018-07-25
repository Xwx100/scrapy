# -*- coding: utf-8 -*-
import scrapy
import os
import re
import html.parser

from io import StringIO
from lxml.html import etree
from testScrapy.yidianzixun.yidian.settings import BASE_DIR
from testScrapy.yidianzixun.yidian.core.parse_csv import ParseCsv

class ToutiaoarticleSpider(scrapy.Spider):
    name = 'toutiaoArticle'
    allowed_domains = ['toutiao.com']
    start_urls = ['http://toutiao.com/']

    def __init__(self, name = None, **kwargs):
        super(ToutiaoarticleSpider,self).__init__(name,**kwargs)
        dir = os.path.join(BASE_DIR, "data/")

        if os.path.exists(dir):
            # 一级目录[[], []]
            self.one_dir = []
            # csv文件列表
            csv_file = []
            # [[(),(),], [(),(),]]
            self.titles_urls = []

            for file in os.listdir(dir):
                if os.path.isfile(dir + file):
                    filename, filend = os.path.splitext(file)
                    if filend == '.csv':
                        csv_dir = dir + filename + r"/"
                        csv_file.append(dir + file)
                        if not os.path.exists(csv_dir):
                            os.makedirs(csv_dir)
                        self.one_dir.append(csv_dir)

            for file in csv_file:
                one_file = []
                parse_csv = ParseCsv(file)
                title_list = parse_csv.extract_csv_title()
                url_list = parse_csv.extract_csv_url()
                for index in range(len(url_list)):
                    one_file.append((title_list[index],url_list[index]))
                self.titles_urls.append(one_file)
            print(self.one_dir)
            print(self.titles_urls)

        else:
            return

    def start_requests(self):
        for index in range(len(self.one_dir)):
            one_dir = self.one_dir[index]
            if not os.path.exists(one_dir):
                os.makedirs(one_dir)
            # image_dir = os.path.join(one_dir,"image")
            # txt_dir = os.path.join(one_dir,"txt")
            # if not os.path.exists(image_dir):
            #     os.makedirs(image_dir)
            # if not os.path.exists(txt_dir):
            #     os.makedirs(txt_dir)

            for title, url in self.titles_urls[index]:
                yield scrapy.Request(
                    url,
                    callback = self.parse_article,
                    meta = {
                        'one_dir': one_dir,
                        'title': title,
                        # 'image_dir': image_dir,
                        # 'txt_dir': txt_dir
                    }
                )

    def parse_article(self, response):
        # response = html.parser.unescape(response.body.decode())
        # print(response)
        s = response.xpath("//body/script[contains(text(),'BASE_DATA')]").extract()
        if s:
            s = s[0]
            article = re.compile(r"content: '(.*);").findall(s)[0]
            article = html.parser.unescape(article)
            article = etree.HTML(article)
            # print(article)
            t = article.xpath("//p/text()|//img/@src")
            txt = ''
            for i in t:
                txt += i.replace(r"\u200b","")
            i = article.xpath("//img/@src")
            print(txt)
            article_dir = response.meta['one_dir'] + r"/" + response.meta['title'] + r"/"
            if not os.path.exists(article_dir):
                os.makedirs(article_dir)
            with open(article_dir + response.meta['title'] + r".txt", "w+", encoding="utf-8") as tFile:
                tFile.write(txt)
            for u in i:
                yield scrapy.Request(
                    u,
                    meta={
                        'article_dir': article_dir,
                    },
                    callback = self.parse_image,
                    dont_filter = True,
                )

    def parse_image(self, response):
        # print(response.headers)
        filename = response.url[-10:]
        with open(response.meta['article_dir'] + r'/' + filename + r".jpeg", "wb+") as image:
            image.write(response.body)




    #
    #
    # def parse(self, response):
    #     pass
