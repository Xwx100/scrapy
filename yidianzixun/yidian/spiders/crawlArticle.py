# -*- coding: utf-8 -*-
import scrapy
import json
import os

from testScrapy.yidianzixun.yidian.settings import BASE_DIR
from testScrapy.yidianzixun.yidian.core.parse_csv import ParseCsv


class CrawlarticleSpider(scrapy.Spider):
    name = 'crawlArticle'
    allowed_domains = ['yidianzixun.com']
    start_urls = ['http://yidianzixun.com/']

    def __init__(self,name=None,**kwargs):
        super(CrawlarticleSpider,self).__init__(name,**kwargs)
        parseCsv = ParseCsv("./html/new.csv")
        self.extract_csv_title = parseCsv.extract_csv_title()
        self.extract_csv_url = parseCsv.extract_csv_url()


    def start_requests(self):
        urls = self.extract_csv_url
        titles = self.extract_csv_title
        print(self.extract_csv_url)
        if len(urls) == len(titles):
            for index in range(len(urls)):
                one_dir = os.path.join(BASE_DIR, r"html/" + titles[index])
                if not os.path.exists(one_dir):
                    os.makedirs(one_dir)

                yield scrapy.Request(
                    urls[index],
                    callback = self.parse_article,
                    meta={
                        'one_dir': one_dir,
                        'title': titles[index]
                    }
                )


    def parse_article(self, response):
        txt_xpath = r"//div//p[not(@class)]/text()|//div/p/a[contains(@href,'channel')]/text()|//div//span/img/@src"
        image_xpath = "//div//span/img/@src"
        
        txt_list = response.xpath(txt_xpath).extract()
        url_list = response.xpath(image_xpath).extract()
        # print(txt_list)
        # print(url_list)
        txt = ''
        for i in txt_list:
            txt += i

        article_dir = response.meta['one_dir'] + r'/'
        print(article_dir)
        with open(article_dir + response.meta['title'] + ".txt", "w+", encoding="utf-8") as t:
            t.write(txt)

        for url in url_list:
            yield scrapy.Request(
                "https:" + url,
                callback = self.parse_image,
                meta = {
                    'article_dir': article_dir,
                },
                dont_filter = True
            )

    def parse_image(self,response):
        filename = response.url[-10:]
        with open(response.meta['article_dir'] + r'/' + filename + ".jpeg", "wb+") as f:
            f.write(response.body)