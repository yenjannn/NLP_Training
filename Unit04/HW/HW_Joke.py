#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# 使用笑話及新聞測試，未知文本是笑話。

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
        
    #articut = Articut(username, apikey, level="lv1")
    articut = Articut(username=userinfoDICT["username"], apikey=userinfoDICT["apikey"])
    
# 已知類別文本：笑話文本 & 新聞文本
    jokeSTR = """去醫院做核酸檢測(PCR)，一位醫生用嚴肅的語氣問我：「你有理由死嗎？還是沒有理由死？」
    聽到這個問題，我沉默了也想了很多，想了家人，想了朋友，想了還沒實現的夢想.....
    最後我堅定的回答：「沒有理由死！」
    醫生聽到我的回答，提筆就寫了「沒有旅遊史」""".replace(" ", "").replace("\n", "")
    
    newsSTR = """松山文創園區宣布7/13起開放，松菸小賣所、風格店家也同步開店營業，在相關管制措施下，
    民眾進入室內場館需配合量體溫、手部消毒、實聯制、全程戴口罩、維持1.5公尺社交距離，同時室內場館禁止飲食。
    而展覽場依中央藝文場館防疫管理措施辦理，餐廳與商店等附屬場域也遵從主管機關及地方政府指示作業。
    另展覽場設置「防疫小組」，進行前置防疫措施與工作人員健康管理。""".replace(" ", "").replace("\n", "")   
    
    HW_JokeDICT = {}
    with open("HW_JokeDICT.json", mode="w", encoding="utf-8") as f:
        json.dump(HW_JokeDICT, f, ensure_ascii=False)
    
    jokeResultDICT = articut.parse(jokeSTR, userDefinedDictFILE="./HW_JokeDICT.json")
    newsResultDICT = articut.parse(newsSTR, userDefinedDictFILE="./HW_JokeDICT.json")
    
    
# 未知類別文本(笑話)
    unknownSTR = """吳國將軍甘興因為一次割東西時，不小心割壞了吳國之主孫權心愛的桌子，孫權很生氣的決定將他斬首，
    這時吳國軍師周瑜就決定想個方法救甘興，於是他讓全國的人在割東西之前先在桌子上墊一張紙，孫權也就因為這個方法原
    諒了甘興，於是這就是全國電子就甘心的由來""".replace(" ", "").replace("\n", "")   
    
    
    
    
# 取得「動詞」做為特徵列表
    jokeVerbLIST = articut.getVerbStemLIST(jokeResultDICT)
    print("笑話文本動詞：")
    print(wordExtractor(jokeVerbLIST, unify=False))
    print("\n")
    newsVerbLIST = articut.getVerbStemLIST(newsResultDICT)
    print("新聞文本動詞：")
    print(wordExtractor(newsVerbLIST, unify=False))
    print("\n")
    unknownResultDICT = articut.parse(unknownSTR, userDefinedDictFILE="./HW_JokeDICT.json")
    unknownVerbLIST = articut.getVerbStemLIST(unknownResultDICT)
    print("未知文本動詞：")
    print(wordExtractor(unknownVerbLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個動詞出現的次數
    jokeCOUNT = Counter(wordExtractor(jokeVerbLIST, unify=False))
    newsCOUNT = Counter(wordExtractor(newsVerbLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownVerbLIST, unify=False))

    # 計算 [笑話文本 vs. 未知文本] 的餘弦相似度；計算 [新聞文本 vs. 未知文本] 的餘弦相似度；
    joke2unknownSIM = counterCosineSimilarity(jokeCOUNT, unknownCOUNT)
    news2unknownSIM = counterCosineSimilarity(newsCOUNT, unknownCOUNT)

    print("[笑話文本 vs. 未知文本] 的動詞餘弦相似度:{}".format(joke2unknownSIM))
    print("[新聞文本 vs. 未知文本] 的動詞餘弦相似度:{}".format(news2unknownSIM))
    print("\n")
    




# 取得「名詞」做為特徵列表
    jokeNounLIST = articut.getNounStemLIST(jokeResultDICT)
    print("笑話文本名詞：")
    print(wordExtractor(jokeNounLIST, unify=False))
    print("\n")
    print("新聞文本名詞：")
    newsNounLIST = articut.getNounStemLIST(newsResultDICT)
    print(wordExtractor(newsNounLIST, unify=False))
    print("\n")
    unknownResultDICT = articut.parse(unknownSTR, userDefinedDictFILE="./HW_JokeDICT.json")
    unknownNounLIST = articut.getNounStemLIST(unknownResultDICT)
    print("未知文本名詞：")
    print(wordExtractor(unknownNounLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個名詞出現的次數
    jokeCOUNT = Counter(wordExtractor(jokeNounLIST, unify=False))
    newsCOUNT = Counter(wordExtractor(newsNounLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownNounLIST, unify=False))

    # 計算 [笑話文本 vs. 未知文本] 的餘弦相似度；計算 [新聞文本 vs. 未知文本] 的餘弦相似度；
    joke2unknownSIM = counterCosineSimilarity(jokeCOUNT, unknownCOUNT)
    news2unknownSIM = counterCosineSimilarity(newsCOUNT, unknownCOUNT)

    print("[笑話文本 vs. 未知文本] 的名詞餘弦相似度:{}".format(joke2unknownSIM))
    print("[新聞文本 vs. 未知文本] 的名詞餘弦相似度:{}".format(news2unknownSIM))
    print("\n")
    
    
    
    
    
# 取得「TF-IDF」做為特徵列表
    jokeTFIDFLIST = articut.analyse.extract_tags(jokeResultDICT)
    print("笑話文本 TF-IDF：")
    print(jokeTFIDFLIST)
    print("\n")
    print("新聞文本 TF-IDF：")
    newsTFIDFLIST = articut.analyse.extract_tags(newsResultDICT)
    print(newsTFIDFLIST)
    print("\n")
    unknownResultDICT = articut.parse(unknownSTR, userDefinedDictFILE="./HW_JokeDICT.json")
    unknownTFIDFLIST = articut.analyse.extract_tags(unknownResultDICT)
    print("未知文本 TF-IDF：")
    print(unknownTFIDFLIST)
    print("\n")


    # 利用 Counter() 模組計算每個 TF-IDF 特徵詞出現的次數
    jokeCOUNT = Counter(jokeTFIDFLIST)
    newsCOUNT = Counter(newsTFIDFLIST)
    unknownCOUNT = Counter(unknownTFIDFLIST)

    # 計算 [笑話文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；計算 [新聞文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；
    joke2unknownSIM = counterCosineSimilarity(jokeCOUNT, unknownCOUNT)
    news2unknownSIM = counterCosineSimilarity(newsCOUNT, unknownCOUNT)

    print("[笑話文本 vs. 未知文本] 的 TF-IDF 特徵詞餘弦相似度:{}".format(joke2unknownSIM))
    print("[新聞文本 vs. 未知文本] 的 TF-IDF 特徵詞餘弦相似度:{}".format(news2unknownSIM))
    
    
    # 取出「人」
    jokePeopleLIST = articut.getPersonLIST(jokeResultDICT)
    print('笑話文本中的「人」:', wordExtractor(jokePeopleLIST))

    newsPeopleLIST = articut.getPersonLIST(newsResultDICT)
    print('新聞文本中的「人」:', wordExtractor(newsPeopleLIST))
    print("\n")

    # 取出「事」
    #jokeEventLIST = articut.parse(jokeSTR, userDefinedDictFILE="./mixedDICT.json", level="lv3")["event"]
    #print('笑話文本中的「事」:', jokeEventLIST)

    #newsEventLIST = articut.parse(newsSTR, userDefinedDictFILE="./mixedDICT.json", level="lv3")["event"]
    #print('新聞文本中的「事」:', newsEventLIST)
    #print("\n")


    # 取出「時」
    #jokeTimeLIST = articut.parse(jokeSTR, userDefinedDictFILE="./mixedDICT.json", level="lv3")["time"]
    #print('笑話文本中的「時」:', jokeTimeLIST)

    #newsTimeLIST = articut.parse(newsSTR, userDefinedDictFILE="./mixedDICT.json", level="lv3")["time"]
    #print('新聞文本中的「時」:', newsTimeLIST)
    #print("\n")


    # 取出「地」
    jokeLocLIST = articut.getLocationStemLIST(jokeResultDICT)
    print('笑話文本中的「地」:', wordExtractor(jokeLocLIST))

    newsLocLIST = articut.getLocationStemLIST(newsResultDICT)
    print('新聞文本中的「地」:', wordExtractor(newsLocLIST))
    print("\n")

    # 取出「物」
    jokeNounLIST = articut.getNounStemLIST(jokeResultDICT)
    print('笑話文本中的「物」:', wordExtractor(jokeNounLIST))

    newsNounLIST = articut.getNounStemLIST(newsResultDICT)
    print('新聞文本中的「物」:', wordExtractor(newsNounLIST))