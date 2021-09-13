#!/usr/bin/env python3
# -*- coding:utf-8 -*-

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

    # 已知類別的文本
    travelSTR = """先省荷包買起來以後再去住！高雄漢來大飯店推出限時「買3送1」優惠，只要一次預訂3間或連住3晚，就送1張平日精緻雙人房住宿券，
    雙人入住換算下來平均每人每晚只要1008元。另外，北部的朋友也有福了，雄獅旅遊首度祭出飯店快閃優惠，台北晶華酒店平日免費升等豪華房，睡1晚下
    殺2折價只要3499元起。""".replace(" ", "").replace("\n", "")

    entertainmentSTR = """南韓女星成宥利是元祖女團Fin.K.L.成員之一，她與由李孝利、玉珠鉉、李真3位近來雖少在節目上合體，但私下感情依舊很好。
    而她2017年嫁給高爾夫球選手安勝賢後，仍活躍在螢光幕前，夫妻倆結婚4年，終於在近來迎來好消息，她親自寫信報喜表示：「我們家庭終於有可愛的孩子
    降臨了，而且不是一個，是雙胞胎。」懷孕喜訊公開後，粉絲也獻上滿滿祝福。""".replace(" ", "").replace("\n", "")


    #travelResultDICT = articut.parse(travelSTR, level='lv2')
    #entertainmentResultDICT = articut.parse(entertainmentSTR, level='lv2')    

    HW_test03DICT = {}
    with open("HW_test03DICT.json", mode="w", encoding="utf-8") as f:
        json.dump(HW_test03DICT, f, ensure_ascii=False)
    
    travelResultDICT = articut.parse(travelSTR, userDefinedDictFILE="./HW_test03DICT.json")
    entertainmentResultDICT = articut.parse(entertainmentSTR, userDefinedDictFILE="./HW_test03DICT.json")
    
    
    # 未知類別的文本
    unknownSTR01 = """確診數連日降新低，飯店業及旅遊平台搶攻「微解封」熱潮。本篇搜羅各飯店最新優惠，包含加價1,000元住一晚、提供快篩陰性證明
    折房價300元、一人免650元就能住一晚，趁此時來趟奢華飯店微旅行，花小錢沉浸在舒適空間，找回內心寧靜力量。""".replace(" ", "").replace("\n", "")    
    
    unknownSTR02 = """《奈良美智特展》高雄站將於7月24日至10月31日在「高雄市立美術館」舉行，因應防疫，全面採「線上預約」實聯制免費參觀，預
    約連結在今（16）日中午13時正式開放，5個步驟即可登記，目前一次開放2週期間登記。""".replace(" ", "").replace("\n", "")
    
    unknownSTR03 = """期待解封日趕快到來嗎？旅遊電商平台KKday即日起至7/23推出「解封樂園夢想包」，只要新台幣1元就有機會抽中全台超過10家人氣
    樂園的門票組合，一人中獎、兩人同行。""".replace(" ", "").replace("\n", "")
    
    unknownSTR04 = """位於苗栗頭份的「鮮肉湯包」，舊舊店面外觀看上去毫不起眼，卻藏著平價又美味的銷魂湯包，是在地人的最愛。湯包邪惡湯汁與迷人
    香氣讓人一口接一口，不論內餡或外皮都頗俱水準，吃貨們絕對不能錯過。""".replace(" ", "").replace("\n", "")
    
    unknownSTR05 = """台東都蘭開有一間神秘低調餐廳，遠離塵囂的悠閒氛圍，令人不自覺的放鬆下來，每天僅接待20組客人，沒預約基本上吃不到，店內招
    牌包括超鮮墨魚麵和香濃燉飯，其中最令老闆自豪的料理，就是他自行研發的超強美式漢堡，就連外國人都慕名來品嚐。""".replace(" ", "").replace("\n", "")
    
    unknownSTR06 = """YouTuber二伯與蔡阿嘎結婚後，育有2個兒子「蔡桃貴」和「蔡波能」，不時會與粉絲分享育兒生活，最近在Instagram被問到是否
    會限制大兒子看3C產品時，她坦言之前的確會讓大兒子玩iPad，結果發現小孩有點沉迷後，她便直接戒斷孩子這個開始養成的習慣。""".replace(" ", "").replace("\n", "")
    
    unknownSTR07 = """雞排妹（鄭家純）被拍到和王先生（保時捷男）出入飯店，但男方爆出已有未婚妻趙小姐（A女），讓她被質疑是第三者，而趙小姐
    事後表示一切非事實，王先生也在16日發出道歉聲明，談到「開放式交友關係」，掀起不少熱議。對此，網路紅人「黑心律師」楊律師就分析出三點王先生
    的聲明內容。""".replace(" ", "").replace("\n", "")
    
    unknownSTR08 = """韓星金鍾國近期開啟個人YouTube頻道《GYM鍾國》，不到一個月時間便突破百萬訂閱。最新企劃中，他找來《RM》夥伴宋智孝合作，
    打算教女方簡單的居家運動，沒想到超嚴格的訓練讓宋智孝累倒在地甚至巴不得想逃跑，兩人有趣的互動也讓大批網友笑翻。""".replace(" ", "").replace("\n", "")
    
    unknownSTR09 = """韓劇《我的室友是九尾狐》昨（16日）晚間劃下句點，尤其張基龍與惠利的組合被稱為最有CP感的螢幕情侶之一，讓人好奇惠利正牌
    男友柳俊烈的心情。而惠利也在訪問中親自證實，「男友每一集都有看，很感謝他。」也證明兩人穩交邁入第5年感情不變。""".replace(" ", "").replace("\n", "")
    
    unknownSTR10 = """南韓體育型綜藝節目《團結才能踢》邀請多位選手對抗明星，有趣又熱血的內容，獲得觀眾青睞，近期開拍第二季。怎料，近來南韓
    疫情升溫，現延燒到演藝圈與體育界，10日參與賽事的選手中鏢感染新冠肺炎，16日更爆出由於超模韓惠珍近期有與排球選手金曜漢接觸，也跟著確診新冠
    肺炎，體育圈、演藝圈疫情拉警報。""".replace(" ", "").replace("\n", "")
    
    
    #unknownResultDICT = articut.parse(unknownSTR01, level='lv2')
    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./HW_test03DICT.json")


    # 取得「動詞」做為特徵列表
    travelVerbLIST = articut.getVerbStemLIST(travelResultDICT)
    print("旅遊新聞文本動詞：")
    print(wordExtractor(travelVerbLIST, unify=False))
    print("\n")
    
    entertainmentVerbLIST = articut.getVerbStemLIST(entertainmentResultDICT)
    print("娛樂新聞文本動詞：")
    print(wordExtractor(entertainmentVerbLIST, unify=False))
    print("\n")
    
    unknownVerbLIST = articut.getVerbStemLIST(unknownResultDICT)
    print("未知文本動詞：")
    print(wordExtractor(unknownVerbLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個動詞出現的次數
    travelCOUNT = Counter(wordExtractor(travelVerbLIST, unify=False))
    entertainmentCOUNT = Counter(wordExtractor(entertainmentVerbLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownVerbLIST, unify=False))

    # 計算 [旅遊新聞文本 vs. 未知文本] 的餘弦相似度；計算 [娛樂新聞文本 vs. 未知文本] 的餘弦相似度；
    travel2unknownSIM = counterCosineSimilarity(travelCOUNT, unknownCOUNT)
    entertainment2unknownSIM = counterCosineSimilarity(entertainmentCOUNT, unknownCOUNT)

    print("[旅遊新聞文本 vs. 未知文本] 的動詞餘弦相似度:{}".format(travel2unknownSIM))
    print("[娛樂新聞文本 vs. 未知文本] 的動詞餘弦相似度:{}".format(entertainment2unknownSIM))
    print("\n")





    # 取得「名詞」做為特徵列表
    travelNounLIST = articut.getNounStemLIST(travelResultDICT)
    print("旅遊新聞文本名詞：")
    print(wordExtractor(travelNounLIST, unify=False))
    print("\n")
    
    entertainmentNounLIST = articut.getNounStemLIST(entertainmentResultDICT)
    print("娛樂新聞文本名詞：")
    print(wordExtractor(entertainmentNounLIST, unify=False))
    print("\n")
    
    unknownNounLIST = articut.getNounStemLIST(unknownResultDICT)
    print("未知文本名詞：")
    print(wordExtractor(unknownNounLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個名詞出現的次數
    travelCOUNT = Counter(wordExtractor(travelNounLIST, unify=False))
    entertainmentCOUNT = Counter(wordExtractor(entertainmentNounLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownNounLIST, unify=False))

    # 計算 [旅遊新聞文本 vs. 未知文本] 的餘弦相似度；計算 [娛樂新聞文本 vs. 未知文本] 的餘弦相似度；
    travel2unknownSIM = counterCosineSimilarity(travelCOUNT, unknownCOUNT)
    entertainment2unknownSIM = counterCosineSimilarity(entertainmentCOUNT, unknownCOUNT)

    print("[旅遊新聞文本 vs. 未知文本] 的名詞餘弦相似度:{}".format(travel2unknownSIM))
    print("[娛樂新聞文本 vs. 未知文本] 的名詞餘弦相似度:{}".format(entertainment2unknownSIM))
    print("\n")




    # 取得「名詞」做為特徵列表
    travelTFIDFLIST = articut.analyse.extract_tags(travelResultDICT)
    print("旅遊新聞文本 TF-IDF：")
    print(travelTFIDFLIST)
    print("\n")
    
    entertainmentTFIDFLIST = articut.analyse.extract_tags(entertainmentResultDICT)
    print("娛樂新聞文本 TF-IDF：")
    print(entertainmentTFIDFLIST)
    print("\n")
    
    unknownTFIDFLIST = articut.analyse.extract_tags(unknownResultDICT)
    print("未知文本 TF-IDF：")
    print(unknownTFIDFLIST)
    print("\n")


    # 利用 Counter() 模組計算每個 TF-IDF 特徵詞出現的次數
    travelCOUNT = Counter(travelTFIDFLIST)
    entertainmentCOUNT = Counter(entertainmentTFIDFLIST)
    unknownCOUNT = Counter(unknownTFIDFLIST)

    # 計算 [旅遊新聞文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；計算 [娛樂新聞文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；
    travel2unknownSIM = counterCosineSimilarity(travelCOUNT, unknownCOUNT)
    entertainment2unknownSIM = counterCosineSimilarity(entertainmentCOUNT, unknownCOUNT)

    print("[旅遊新聞文本 vs. 未知文本] 的 TF-IDF 特徵詞餘弦相似度:{}".format(travel2unknownSIM))
    print("[娛樂新聞文本 vs. 未知文本] 的 TF-IDF 特徵詞餘弦相似度:{}".format(entertainment2unknownSIM))
    print("\n")




    # 取出「人」
    travelPeopleLIST = articut.getPersonLIST(travelResultDICT)
    print('旅遊新聞文本中的「人」:', wordExtractor(travelPeopleLIST))

    entertainmentPeopleLIST = articut.getPersonLIST(entertainmentResultDICT)
    print('娛樂新聞文本中的「人」:', wordExtractor(entertainmentPeopleLIST))
    print("\n")

    # 取出「事」
    #travelEventLIST = articut.parse(travelSTR, userDefinedDictFILE="./mixedDICT.json", level="lv3")["event"]
    #print('旅遊新聞文本中的「事」:', travelEventLIST)

    #entertainmentEventLIST = articut.parse(entertainmentSTR, userDefinedDictFILE="./mixedDICT.json", level="lv3")["event"]
    #print('娛樂新聞文本中的「事」:', entertainmentEventLIST)
    #print("\n")


    # 取出「時」
    #travelTimeLIST = articut.parse(travelSTR, userDefinedDictFILE="./mixedDICT.json", level="lv3")["time"]
    #print('旅遊新聞文本中的「時」:', travelTimeLIST)

    #entertainmentTimeLIST = articut.parse(entertainmentSTR, userDefinedDictFILE="./mixedDICT.json", level="lv3")["time"]
    #print('娛樂新聞文本中的「時」:', entertainmentTimeLIST)
    #print("\n")


    # 取出「地」
    travelLocLIST = articut.getLocationStemLIST(travelResultDICT)
    print('旅遊新聞文本中的「地」:', wordExtractor(travelLocLIST))

    entertainmentLocLIST = articut.getLocationStemLIST(entertainmentResultDICT)
    print('娛樂新聞文本中的「地」:', wordExtractor(entertainmentLocLIST))
    print("\n")

    # 取出「物」
    travelNounLIST = articut.getNounStemLIST(travelResultDICT)
    print('旅遊新聞文本中的「物」:', wordExtractor(travelNounLIST))

    entertainmentNounLIST = articut.getNounStemLIST(entertainmentResultDICT)
    print('娛樂新聞文本中的「物」:', wordExtractor(entertainmentNounLIST))