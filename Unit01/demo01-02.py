#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from ArticutAPI import Articut
from pprint import pprint
import json

if __name__ == "__main__":
    with open("account.info", encoding="utf-8") as f:
        userinfoDICT = json.loads(f.read())
        
    #articut = Articut(username, apikey, level="lv1")
    articut = Articut(username=userinfoDICT["username"], apikey=userinfoDICT["apikey"])    

    inputSTR = "小紅帽"
    resultDICT = articut.parse(inputSTR, level="lv1") #注意 level 參數設定為 "lv1"
    print("\n lv1 的設定下，處理結果：\n", resultDICT)

    resultDICT = articut.parse(inputSTR, level="lv2") #注意 level 參數設定為 "lv2"
    print("\n lv2 的設定下，處理結果：\n", resultDICT)