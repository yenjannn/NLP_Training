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

    inputSTR = "會被大家盯上，才證明你有實力"
    resultDICT = articut.parse(inputSTR)
    pprint(resultDICT)