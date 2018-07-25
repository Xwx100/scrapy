# -*- coding: utf-8 -*-
import jieba.posseg as psg
import re
from gensim import corpora,models,similarities

class ArticleSimilarity(object):

    def __init__(self, flags=True):
        if flags==True or not isinstance(flags,list):
            # [字符串、标点符号、连词、助词、副词、介词、时语素、‘的’、数词、方位词、代词]
            self.stop_flags = ['x', 'w', 'c', 'u','d', 'p', 't', 'uj', 'm', 'f', 'r']
        else:
            self.stop_flags= flags

    def titleSimilarity(self, query, txt):
        query_list, doc_list = self.tokenization_two(query, txt)
        documents = self.documents(doc_list)
        dictionary = self.dictionary(documents)
        # print(dictionary.token2id)
        corpus = self.corpus(documents)
        # print(corpus)
        query_vec = self.query_vec(documents, query_list)
        tfidf = self.tfidf(corpus)
        s = self.tfidf_sim(tfidf, corpus, dictionary, query_vec)
        return int(s[-1] * 100)

    def articleSimilarity(self, query, txt):
        documents = [['']]
        if len(txt)==1:
            documents.append(txt[0])
        else:
            documents = txt
        dictionary = self.dictionary(documents)
        # print(dictionary.token2id)
        corpus = self.corpus(documents)
        print(corpus)
        query_vec = self.query_vec(documents, query)
        print(query_vec)
        tfidf = self.tfidf(corpus)
        s = self.tfidf_sim(tfidf, corpus, dictionary, query_vec)
        return s

    def article_lsi(self, query, txt):
        documents = [['']]
        if len(txt)==1:
            documents.append(txt[0])
        else:
            documents = txt
        dictionary = self.dictionary(documents)
        corpus = self.corpus(documents)
        query_vec = self.query_vec(documents, query)
        tfidf = self.tfidf(corpus)
        lsi = self.lsi(tfidf, corpus, dictionary)
        query_lsi = self.query_lsi(query_vec, lsi)
        s = self.lsi_sim(tfidf, corpus, dictionary, query_lsi, lsi)
        return s




    # @ return: ([,], [,])
    def tokenization_two(self, query, txt):
        if isinstance(query, str) and isinstance(txt, str):
            query_list, txt_list = self.tokenization_one(query), self.tokenization_one(txt)
            return query_list, txt_list

    # @return: [,]
    def tokenization_one(self, txt, only_chinese = False):
        if isinstance(txt, str):
            txt_list = []
            if only_chinese:
                s_l = re.compile(r"[\u4e00-\u9fff]+").findall(txt)
                ss = ''
                for i in s_l:
                    ss += i
                txt = ss
            txt_words = psg.cut(txt)
            for word,flag in txt_words:
                if flag not in self.stop_flags:
                    txt_list.append(word)
            return txt_list
        else:
            return []

    # 查询一个相似度才需要这方法，在前面添加空字符串
    # @return: [[''],]
    def documents(self, txt_list):
        documents = [[''],]
        if isinstance(txt_list, list):
            documents.append(txt_list)
            return documents


    # @return: dictionary
    def dictionary(self, documents):
        dictionary = corpora.Dictionary(documents)
        return dictionary

    # @return corpus
    def corpus(self,documents):
        corpus = [self.dictionary(documents).doc2bow(doc) for doc in documents]
        return corpus

    # @return query_vec
    def query_vec(self, documents, query_documents):
        query_vec = self.dictionary(documents).doc2bow(query_documents)
        return query_vec

    # @return tfidf
    def tfidf(self,corpus):
        tfidf = models.TfidfModel(corpus)
        return tfidf

    # @return sim
    def tfidf_sim(self, tfidf, corpus, dictionary, query_vec):
        index = similarities.MatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))
        sim = index[tfidf[query_vec]]
        return sim

    def lsi(self, tfidf, corpus, dictionary):
        lsi = models.LsiModel(tfidf[corpus], id2word= dictionary)
        return lsi

    def query_lsi(self, query_vec, lsi):
        query_lsi = lsi[query_vec]
        return query_lsi

    def lsi_sim(self, tfidf, corpus, dictionary, query_lsi, lsi):
        lsi_vec = lsi[tfidf[corpus]]
        index = similarities.MatrixSimilarity(lsi_vec, num_features=len(dictionary.keys()))
        sim = index[query_lsi]
        return sim




