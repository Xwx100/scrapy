
import csv

class ParseCsv(object):
    """处理首行为key，其他行为value的csv"""

    def __init__(self,filename):
        self.filename = filename

    # @yidian_dict [{key:value,key:value,...},]
    def parse_csv(self):
        yidian_dict = []
        with open(self.filename, "r+", encoding="utf-8") as yidian:
            yidianReader = csv.reader(yidian)
            fieldnames = next(yidianReader)
            if fieldnames:
                yidianReader = csv.DictReader(yidian, fieldnames=fieldnames)
                for yidian in yidianReader:
                    w_dict = {}
                    for key, value in yidian.items():
                        w_dict[key] = value
                    yidian_dict.append(w_dict)
        return yidian_dict

    def extract_csv_url(self):
        article_list = self.parse_csv()
        url_list = []
        for url in article_list:
            url_list.append(url['文章链接'])
        return url_list

    def extract_csv_title(self):
        article_list = self.parse_csv()
        header_list = []
        for article in article_list:
            header_list.append(article['文章标题'])
        return header_list