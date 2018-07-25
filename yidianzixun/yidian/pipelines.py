# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import os
from testScrapy.yidianzixun.yidian.settings import BASE_DIR


class YidianPipeline(object):

    _yidian_list = []
    def __init__(self):
        print('---Yidian--init---')

    def process_item(self, item, spider):
        print(spider.name)
        if spider.name in "yidian":
            item = dict(item)
            html_dir = os.path.join(BASE_DIR, "html")
            if not os.path.exists(html_dir):
                os.makedirs(html_dir)
            with open("./html/new.csv", "a+", newline="", encoding="utf-8") as yidian_f:
                yidian_w = csv.writer(yidian_f)
                yidian_row = ['文章标题', '文章小时', '文章评论数', '文章类别', '文章类型', '文章链接']
                if next(csv.reader(open("./html/new.csv", "r+", newline="", encoding="utf-8")), None) != yidian_row:
                    yidian_w.writerow(yidian_row)

                self._yidian_list.append(item.values())
                if item.values() not in self._yidian_list:
                    yidian_w.writerow(item.values())
                yidian_f.close()

        if spider.name in "toutiao":
            dir = os.path.join(BASE_DIR, 'data/')
            if not os.path.isdir(dir):
                os.makedirs(dir)
            item = dict(item)
            filename = item.pop('filename')
            filename = r"./data/" + filename + r".csv"
            with open(filename, "a+", newline='', encoding='utf-8') as toutiao_f:
                toutiao_w = csv.writer(toutiao_f)
                toutiao_row = ['文章标题', '文章日期', '文章评论数', '文章作者', '标题相似度', '文章链接']
                if next(csv.reader(open(filename, "r+", newline="", encoding="utf-8")), None) != toutiao_row:
                    toutiao_w.writerow(toutiao_row)
                toutiao_w.writerow(item.values())
                toutiao_f.close()

    def open_spider(self,spider):
        print(spider.name)
        print('-----open_spider-----')

    def close_spider(self,spider):
        print('-------close_spider------------')

