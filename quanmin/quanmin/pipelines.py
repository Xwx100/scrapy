# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import os

from . import settings
from scrapy.pipelines.images import ImagesPipeline


class QuanminPipeline(ImagesPipeline):
    IMAGES_STORE = settings.IMAGES_STORE

    def get_media_requests(self, item, info):
        image_url = item['image_url']
        yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok,x in results if ok]
        os.rename(self.IMAGES_STORE + "/" + image_path[0],
                  self.IMAGES_STORE + '/' + item['name'] + '-' + item['people'] + '.jpg')

