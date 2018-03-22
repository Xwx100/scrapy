# -*- coding: utf-8 -*-
import scrapy
from quanmin.items import QuanminItem

class QuanminSpider(scrapy.Spider):
    name = 'Quanmin'
    allowed_domains = ['quanmin.tv']
    start_urls = ['https://www.quanmin.tv/game/showing']

    def parse(self, response):
        image_url_list = response.xpath("//div[@class='list_w-card-showing_cover-wrap']/img/@src").extract()
        name_list = response.xpath("//div[@class='list_w-card-showing_info']/span[1]/text()").extract()
        people_list = response.xpath("//div[@class='list_w-card-showing_info']/span[2]/text()").extract()

        for each in range(len(image_url_list)):
            items = QuanminItem()
            items["image_url"] = image_url_list[each]
            items["name"] = name_list[each]
            items["people"] = people_list[each]
            yield items