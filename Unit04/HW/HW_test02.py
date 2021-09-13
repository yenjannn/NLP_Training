#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# 使用整理好的刑事判決書(違反毒品危害防制條例、叛亂、竊盜)。
# 違反毒品危害防制條例:drug.json, 叛亂:rebel.json, 竊盜:theft.json


from collections import Counter
from ArticutAPI import Articut
import json
import math

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
    f.close()
    
    k = 0
    u = 2
    
# 已知類別文本：叛亂判決書文本 & 竊盜判決書文本
    with open("rebel.json", encoding="utf-8") as f:
        STR01LIST = json.loads(f.read())
        STR01 = STR01LIST[k].replace(" ", "").replace("\n", "").replace("\r", "").replace("\u3000", "")
# 未知類別文本(叛亂)        
        unknownSTR = STR01LIST[u].replace(" ", "").replace("\n", "").replace("\r", "").replace("\u3000", "")
    f.close()
    with open("theft.json", encoding="utf-8") as f:
        STR02LIST = json.loads(f.read())
        STR02 = STR02LIST[k].replace(" ", "").replace("\n", "").replace("\r", "").replace("\u3000", "")
    f.close()
    
# 展示文本內容
    print("叛亂判決書文本：")
    print(STR01LIST[k])
    print("\n")
    print("竊盜判決書文本：")
    print(STR02LIST[k])          
    print("\n")
    print("未知類別文本(小抄:叛亂)：")
    print(STR01LIST[u])
    print("\n")
    
    
    HW_test02DICT = {}
    with open("HW_test02DICT.json", mode="w", encoding="utf-8") as f:
        json.dump(HW_test02DICT, f, ensure_ascii=False)
    
    STR01ResultDICT = articut.parse(STR01, userDefinedDictFILE="./HW_test02DICT.json")
    STR02ResultDICT = articut.parse(STR02, userDefinedDictFILE="./HW_test02DICT.json")
    
    
    
    
    
# 取得「動詞」做為特徵列表
    STR01VerbLIST = articut.getVerbStemLIST(STR01ResultDICT)
    print("叛亂判決書文本動詞：")
    print(wordExtractor(STR01VerbLIST, unify=False))
    print("\n")
    STR02VerbLIST = articut.getVerbStemLIST(STR02ResultDICT)
    print("竊盜判決書文本動詞：")
    print(wordExtractor(STR02VerbLIST, unify=False))
    print("\n")
    unknownResultDICT = articut.parse(unknownSTR, userDefinedDictFILE="./HW_test02DICT.json")
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

    print("[叛亂判決書文本 vs. 未知文本] 的動詞餘弦相似度:{}".format(STR012unknownSIM))
    print("[竊盜判決書文本 vs. 未知文本] 的動詞餘弦相似度:{}".format(STR022unknownSIM))
    print("\n")
    
    
    
# 取得「名詞」做為特徵列表
    STR01NounLIST = articut.getNounStemLIST(STR01ResultDICT)
    print("叛亂判決書文本名詞：")
    print(wordExtractor(STR01NounLIST, unify=False))
    print("\n")
    print("竊盜判決書文本名詞：")
    STR02NounLIST = articut.getNounStemLIST(STR02ResultDICT)
    print(wordExtractor(STR02NounLIST, unify=False))
    print("\n")
    unknownResultDICT = articut.parse(unknownSTR, userDefinedDictFILE="./HW_test02DICT.json")
    unknownNounLIST = articut.getNounStemLIST(unknownResultDICT)
    print("未知文本名詞：")
    print(wordExtractor(unknownNounLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個名詞出現的次數
    STR01COUNT = Counter(wordExtractor(STR01NounLIST, unify=False))
    STR02COUNT = Counter(wordExtractor(STR02NounLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownNounLIST, unify=False))

    # 計算 [叛亂判決書文本 vs. 未知文本] 的餘弦相似度；計算 [竊盜判決書文本 vs. 未知文本] 的餘弦相似度；
    STR012unknownSIM = counterCosineSimilarity(STR01COUNT, unknownCOUNT)
    STR022unknownSIM = counterCosineSimilarity(STR02COUNT, unknownCOUNT)

    print("[叛亂判決書文本 vs. 未知文本] 的名詞餘弦相似度:{}".format(STR012unknownSIM))
    print("[竊盜判決書文本 vs. 未知文本] 的名詞餘弦相似度:{}".format(STR022unknownSIM))
    print("\n")
    
    
    
    
    
# 取得「TF-IDF」做為特徵列表
    STR01TFIDFLIST = articut.analyse.extract_tags(STR01ResultDICT)
    print("叛亂判決書文本 TF-IDF：")
    print(STR01TFIDFLIST)
    print("\n")
    print("竊盜判決書文本 TF-IDF：")
    STR02TFIDFLIST = articut.analyse.extract_tags(STR02ResultDICT)
    print(STR02TFIDFLIST)
    print("\n")
    unknownResultDICT = articut.parse(unknownSTR, userDefinedDictFILE="./HW_test02DICT.json")
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

    print("[叛亂判決書文本 vs. 未知文本] 的 TF-IDF 特徵詞餘弦相似度:{}".format(STR012unknownSIM))
    print("[竊盜判決書文本 vs. 未知文本] 的 TF-IDF 特徵詞餘弦相似度:{}".format(STR022unknownSIM))