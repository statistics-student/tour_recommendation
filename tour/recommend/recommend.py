# -*- coding: utf-8 -*-
# @Time : 2020/5/15 3:28
# @Author :
# @File : recommend.py
# @Software: PyCharm
import sys
sys.path.append("..")
import os

from tour.models import *
from django.contrib.auth.models import User

import jieba
from .tfidf import TFIDF
from .cosine import Cosine

def make_recommend(data_source, aim_data):
    '''
    计算推荐
    '''
    # 处理数据
    # comments, goods = get_data()
    # comment_words = split_word(comments)
    descs = data_source
    descs.insert(0, aim_data)
    desc_words = split_word(descs)
    # tf-idf向量化
    tfidf = TFIDF(desc_words, max_words=100)
    desc_model = tfidf.fit_transform()
    # 余弦相似度计算
    consine = Cosine(n_recommendation=20)
    indices, similarities = consine.cal_similarity(desc_model)
    return indices,similarities, descs

def get_data(user_name = "zhanglei"):
    '''
    加载数据
    '''
    #所有评论数据
    data_list = []
    collection_list = []
    for item in View.objects.values("view_desc"):
        data_list.append(item['view_desc'])
    for item in User.objects.filter(username=user_name).values('id'):
        userid = item['id']
    for item in Collection.objects.filter(user_id = userid).values("view_id"):
        for item_2 in View.objects.filter(id= item['view_id']).values("view_desc"):
            collection_list.append(item_2['view_desc'])

    recommed_pairs = []
    for item in collection_list:

        indices, similarties, descs = make_recommend(data_list, item)
        i = 0
        for rec_index in indices[0]:
            if descs[rec_index] not in collection_list:
                recommed_pairs.append((descs[rec_index], similarties[0][i]))
            i += 1

    recommed_result = []
    for item in recommed_pairs:
        if item[0] not in recommed_result:
            recommed_result.append(item[0])

    return recommed_result








def split_word(lines):
    '''
    分词
    '''
    with open(os.path.join(os.getcwd(), "tour/recommend/stopwords.txt"), encoding="utf-8") as f:
        stopwords = f.read().split("\n")
    words_list = []
    for line in lines:
        words = [word for word in jieba.cut(line.strip().replace("\n", "").replace("\r", "").replace("\ue40c", "")) if word not in stopwords]
        words_list.append(" ".join(words))
    return words_list

if __name__ == "__main__":



    for i in range(10):
        comment = comments[i]
        good = goods[i]
        index = indices[i]
        similarity = similarities[i]
        print("当前评论为:\n\'{}\'\n对应的商品名称为:\n{}\n推荐的商品为:\n".format(comment, good))
        axis_goods = []
        for idx, sim in zip(index, similarity):
            if goods[idx] == good or goods[idx] in axis_goods:
                continue
            else:
                axis_goods.append(goods[idx])
                print("\t\t{}, 概率{}\n=================================".format(goods[idx], sim))
        print()

