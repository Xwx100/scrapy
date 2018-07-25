
import os
import gc
from testScrapy.yidianzixun.article_lsi_simi import write_simi

def main():
    os.system("scrapy crawl yidian")
    # os.system("scrapy crawl toutiao")
    # os.system("scrapy crawl crawlArticle")
    # os.system("scrapy crawl toutiaoArticle")
    # write_simi()
    # gc.collect()

if __name__ == '__main__':
    main()