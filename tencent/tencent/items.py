# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentItem(scrapy.Item):
    # define the fields for your item here like:
    # 职位名称
    position_name = scrapy.Field()
    # 职位链接
    position_link = scrapy.Field()
    # 职位类别
    position_type = scrapy.Field()
    # 职位人数
    position_people = scrapy.Field()
    # 职位地址
    position_add = scrapy.Field()
    # 发布时间
    position_time = scrapy.Field()

