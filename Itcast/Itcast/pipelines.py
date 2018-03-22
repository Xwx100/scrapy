# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class ItcastPipeline(object):
    """处理itcast生成的item元素"""
    def __init__(self):
        # 以utf-8编码打开文件
        self.filename = open('teachers.csv','wb+')

    def process_item(self, item, spider):
        # item为unicode编码
        json_text = json.dumps(dict(item),ensure_ascii=False)
        self.filename.write(json_text.encode('utf-8'))
        # 在输出窗口打印
        return item

    def close_spider(self, spider):
        self.filename.close()
