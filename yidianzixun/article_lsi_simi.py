
import os
import csv
from shutil import rmtree

from testScrapy.yidianzixun.yidian.core.article_simillarity import ArticleSimilarity
from testScrapy.yidianzixun.yidian.settings import BASE_DIR
from testScrapy.yidianzixun.yidian.core.parse_csv import ParseCsv

html_dir = os.path.join(BASE_DIR, 'html/')
data_dir = os.path.join(BASE_DIR, "data/")
def lsi_simi():
    t = ArticleSimilarity()

    parse_csv = ParseCsv(html_dir + "/new.csv")
    title_list = parse_csv.extract_csv_title()
    # print(title_list)

    doc_test = []
    docs = []
    all_s = []

    for title in title_list:

        t_dir = os.path.join(html_dir, title)
        t_di = os.path.join(data_dir, title)
        doc = []

        l = os.listdir(t_dir)
        for i in l:
            filename, filend = os.path.splitext(i)
            if filend == '.txt':
                with open(t_dir + r"/" + i, "r+", encoding="utf-8") as f:
                    doc_test.append(t.tokenization_one(f.read(), only_chinese=True))

        for k in os.listdir(t_di):
            f = t_di + "/" + k + "/"
            if os.path.isdir(f):
                for j in os.listdir(f):
                    filename_one, filend_one = os.path.splitext(j)
                    if filend_one == ".txt":
                        # print(f + j)
                        with open(f + j, "r", encoding="utf-8") as fo:
                            doc.append(t.tokenization_one(fo.read(), only_chinese=True))
        if doc==[]:
            doc = [['']]
        docs.append(doc)
        # print(docs)
    # print(docs)
    for index in range(len(doc_test)):
        print(doc_test[index], docs[index])
        s = t.article_lsi(doc_test[index], docs[index])
        a = sorted(enumerate(s), key=lambda item: -item[-1])
        all_s.append(a[0])
    print(all_s)
    return all_s

    # {'一点文章', '一点文章链接', '头条文章', '头条文章链接', '文章相似度'}
    # 一点文章列表： 从new.csv获取
    # 一点文章链接：从new.csv获取
    # 头条文章：根据一点文章列表，查询相应csv，然后根据all_s的下标寻找相似度最高的文章
    # 头条文章链接：类似上
    # 文章相似度：根据all_s输出
def deal_all_s():
    all_s = lsi_simi()

    new_csv = html_dir + "new.csv"
    parse_csv = ParseCsv(new_csv)
    title_list = parse_csv.extract_csv_title()
    url_list = parse_csv.extract_csv_url()

    simi_list = []

    for index in range(len(all_s)):
        # print(all_s[index])
        t_index, simi = all_s[index]
        simi = int(simi*100)
        # print(t_index,simi)
        p_c_o = ParseCsv(data_dir + title_list[index] + ".csv")
        t_list = p_c_o.extract_csv_title()
        u_list = p_c_o.extract_csv_url()
        if simi <= 100:
            try:
                toutiao_title = t_list[t_index]
                toutiao_url = u_list[t_index]
            except:
                toutiao_title = '标题相似都低，不进行对比文章'
                toutiao_url = '标题相似都低，不进行对比文章'
            yidian_title = title_list[index]
            yidian_url = url_list[index]
                # yidian_title = '标题相似都低，不进行对比文章'
                # yidian_url = '标题相似都低，不进行对比文章'

            simi_dict = {}
            simi_dict['一点文章'] = yidian_title
            simi_dict['一点文章链接'] = yidian_url
            simi_dict['头条文章'] = toutiao_title
            simi_dict['头条文章链接'] = toutiao_url
            simi_dict['文章相似度'] = simi
            simi_list.append(simi_dict)
    print(simi_list)
    return simi_list

def write_simi():
    simi_list = deal_all_s()
    # print(simi_list)
    with open("./result.csv", "w+", encoding="utf-8", newline='') as f:
        f_w = csv.writer(f)
        if simi_list:
            f_w.writerow(simi_list[0].keys())
            for row in simi_list:
                f_w.writerow(row.values())
        else:
            f_w.writerow(['无相似度低的文章'])

    d = input("您是否要删除所产生的数据分析(1是,0否)： ")
    if int(d) > 0:
        for i in os.listdir(data_dir):
            if os.path.isdir(data_dir + i):
                rmtree(data_dir + i)
            else:
                os.remove(data_dir + i)
        for i in os.listdir(html_dir):
            if os.path.isdir(html_dir + i):
                rmtree(html_dir + i)
            else:
                os.remove(html_dir + i)
    else:
        return







