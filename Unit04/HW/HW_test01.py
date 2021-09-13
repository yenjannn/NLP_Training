#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# 使用刑事判決書及棒球文本測試，未知文本是棒球類。
# 直接讀入該判決書的json檔。

from collections import Counter
from ArticutAPI import Articut
import json
import math

from pprint import pprint


def wordExtractor(inputLIST, unify=True):
    '''
    配合 Articut() 的 .getNounStemLIST() 和 .getVerbStemLIST() …等功能，拋棄位置資訊，只抽出詞彙。
    '''
    resultLIST = []
    for i in inputLIST:
        if i == []:
            pass
        else:
            for e in i:
                resultLIST.append(e[-1])
    if unify == True:
        return sorted(list(set(resultLIST)))
    else:
        return sorted(resultLIST)

def counterCosineSimilarity(counter01, counter02):
    '''
    計算 counter01 和 counter02 兩者的餘弦相似度
    '''
    terms = set(counter01).union(counter02)
    dotprod = sum(counter01.get(k, 0) * counter02.get(k, 0) for k in terms)
    magA = math.sqrt(sum(counter01.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(counter02.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)


def lengthSimilarity(counter01, counter02):
    '''
    計算 counter01 和 counter02 兩者在長度上的相似度
    '''

    lenc1 = sum(iter(counter01.values()))
    lenc2 = sum(iter(counter02.values()))
    return min(lenc1, lenc2) / float(max(lenc1, lenc2))


if __name__ == "__main__":
    with open("account.info", encoding="utf-8") as f:
        userinfoDICT = json.loads(f.read())
        
    articut = Articut(username=userinfoDICT["username"], apikey=userinfoDICT["apikey"])
    
# 已知類別文本：判決書文本 & 棒球文本
    with open("..\司法院－刑事補償\刑事_97,台重覆,1_2008-02-26.json", encoding="utf-8") as f:
        STR01DICT = json.loads(f.read())
        STR01 = STR01DICT['judgement']
    STR02 = """本週三在紐約的比賽中，馬林魚此戰使用投手車輪戰，4名投手輪番上陣壓制大都會打線，前8局僅被敲出4支安打失1分，
    讓球隊能帶著2-1的領先優勢進入到9局下半。不過馬林魚推出巴斯登板關門，他面對首名打者麥尼爾，就被打出一發陽春砲，
    讓大都會追平比數，接下來又分別被敲出2支安打、投出保送，形成滿壘局面，此時輪到康福托上場打擊。在2好1壞的局面下，
    巴斯投了一顆內角滑球，康福托眼看這顆球越來越靠近自己的身體，似乎有下意識地將手伸進好球帶內，結果這球就直接碰觸到
    他的身肘，隨後主審庫爾帕判定這是一記觸身球，讓大都會兵不血刃拿下再見分，最終贏得比賽勝利。""".replace(" ", "").replace("\n", "")    
    
    HW_test01DICT = {}
    with open("HW_test01DICT.json", mode="w", encoding="utf-8") as f:
        json.dump(HW_test01DICT, f, ensure_ascii=False)
    
    STR01ResultDICT = articut.parse(STR01, userDefinedDictFILE="./HW_test01DICT.json")
    STR02ResultDICT = articut.parse(STR02, userDefinedDictFILE="./HW_test01DICT.json")
    
    
# 未知類別文本(棒球)
    unknownSTR = """金鶯隊左投John Means今天在面對水手隊比賽中，完成一項大紀錄，那就是以27個出局數，
    在沒有保送、觸身球、失誤的狀況下完成無安打比賽，而John Means差一點就有完全比賽，主要是3局下對Sam Haggerty
    投出不死三振，差點就可以完成「完全比賽」，金鶯最終以6:0贏球。根據紀錄，金鶯隊上次左投投出無安打比賽已經是1969年，
    也是大聯盟本季第三場無安打比賽，球隊史上第10位投出無安打比賽的投手，而他也是第一位在沒有投出保送、安打、失誤，
    卻投出無安打比賽的投手。""".replace(" ", "").replace("\n", "")   
    

# 展示刑事判決書文本
    print("刑事判決書文本：")
    pprint(STR01DICT)
    print("\n")    
    
    
    
    
# 取得「動詞」做為特徵列表
    STR01VerbLIST = articut.getVerbStemLIST(STR01ResultDICT)
    print("刑事判決書動詞：")
    print(wordExtractor(STR01VerbLIST, unify=False))
    print("\n")
    STR02VerbLIST = articut.getVerbStemLIST(STR02ResultDICT)
    print("棒球文本動詞：")
    print(wordExtractor(STR02VerbLIST, unify=False))
    print("\n")
    unknownResultDICT = articut.parse(unknownSTR, userDefinedDictFILE="./HW_test01DICT.json")
    unknownVerbLIST = articut.getVerbStemLIST(unknownResultDICT)
    print("未知文本動詞：")
    print(wordExtractor(unknownVerbLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個動詞出現的次數
    STR01COUNT = Counter(wordExtractor(STR01VerbLIST, unify=False))
    STR02COUNT = Counter(wordExtractor(STR02VerbLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownVerbLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    STR012unknownSIM = counterCosineSimilarity(STR01COUNT, unknownCOUNT)
    STR022unknownSIM = counterCosineSimilarity(STR02COUNT, unknownCOUNT)

    print("[刑事判決書文本 vs. 未知文本] 的動詞餘弦相似度:{}".format(STR012unknownSIM))
    print("[棒球文本 vs. 未知文本] 的動詞餘弦相似度:{}".format(STR022unknownSIM))
    print("\n")
    
    
    
    
# 取得「名詞」做為特徵列表
    STR01NounLIST = articut.getNounStemLIST(STR01ResultDICT)
    print("刑事判決書文本名詞：")
    print(wordExtractor(STR01NounLIST, unify=False))
    print("\n")
    print("棒球文本名詞：")
    STR02NounLIST = articut.getNounStemLIST(STR02ResultDICT)
    print(wordExtractor(STR02NounLIST, unify=False))
    print("\n")
    unknownResultDICT = articut.parse(unknownSTR, userDefinedDictFILE="./HW_test01DICT.json")
    unknownNounLIST = articut.getNounStemLIST(unknownResultDICT)
    print("未知文本名詞：")
    print(wordExtractor(unknownNounLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個名詞出現的次數
    STR01COUNT = Counter(wordExtractor(STR01NounLIST, unify=False))
    STR02COUNT = Counter(wordExtractor(STR02NounLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownNounLIST, unify=False))

    # 計算 [刑事判決書文本 vs. 未知文本] 的餘弦相似度；計算 [棒球文本 vs. 未知文本] 的餘弦相似度；
    STR012unknownSIM = counterCosineSimilarity(STR01COUNT, unknownCOUNT)
    STR022unknownSIM = counterCosineSimilarity(STR02COUNT, unknownCOUNT)

    print("[刑事判決書文本 vs. 未知文本] 的名詞餘弦相似度:{}".format(STR012unknownSIM))
    print("[棒球文本 vs. 未知文本] 的名詞餘弦相似度:{}".format(STR022unknownSIM))
    print("\n")
    
    
    
    
    
# 取得「TF-IDF」做為特徵列表
    STR01TFIDFLIST = articut.analyse.extract_tags(STR01ResultDICT)
    print("刑事判決書文本 TF-IDF：")
    print(STR01TFIDFLIST)
    print("\n")
    print("棒球文本 TF-IDF：")
    STR02TFIDFLIST = articut.analyse.extract_tags(STR02ResultDICT)
    print(STR02TFIDFLIST)
    print("\n")
    unknownResultDICT = articut.parse(unknownSTR, userDefinedDictFILE="./HW_test01DICT.json")
    unknownTFIDFLIST = articut.analyse.extract_tags(unknownResultDICT)
    print("未知文本 TF-IDF：")
    print(unknownTFIDFLIST)
    print("\n")


    # 利用 Counter() 模組計算每個 TF-IDF 特徵詞出現的次數
    STR01COUNT = Counter(STR01TFIDFLIST)
    STR02COUNT = Counter(STR02TFIDFLIST)
    unknownCOUNT = Counter(unknownTFIDFLIST)

    # 計算 [刑事判決書文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；計算 [棒球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；
    STR012unknownSIM = counterCosineSimilarity(STR01COUNT, unknownCOUNT)
    STR022unknownSIM = counterCosineSimilarity(STR02COUNT, unknownCOUNT)

    print("[刑事判決書文本 vs. 未知文本] 的 TF-IDF 特徵詞餘弦相似度:{}".format(STR012unknownSIM))
    print("[棒球文本 vs. 未知文本] 的 TF-IDF 特徵詞餘弦相似度:{}".format(STR022unknownSIM))