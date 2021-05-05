#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from ArticutAPI import Articut
from pprint import pprint


if __name__ == "__main__":
    username = "peter.w@droidtown.co"
    apikey   = "pEWjfx317g!zhLnU6W^hnWeyirr&JR6"

    articut = Articut(username, apikey)

    inputBaseballSTR = """馬林魚此戰使用投手車輪戰，4名投手輪番上陣壓制大都會打線，
    前8局僅被敲出4支安打失1分，讓球隊能帶著2-1的領先優勢進入到9局下半。不過馬林魚推出
    巴斯登板關門，他面對首名打者麥尼爾，就被打出一發陽春砲，讓大都會追平比數，接下來又
    分別被敲出2支安打、投出保送，形成滿壘局面，此時輪到康福托上場打擊。在2好1壞的局面
    下，巴斯投了一顆內角滑球，康福托眼看這顆球越來越靠近自己的身體，似乎有下意識地將手
    伸進好球帶內，結果這球就直接碰觸到他的身肘，隨後主審庫爾帕判定這是一記觸身球，讓
    大都會兵不血刃拿下再見分，最終贏得比賽勝利。"""

    inputBasketballSTR = """錯失勝利的太陽沒有就此束手就擒，延長賽一開始就打出7比2攻勢，
    米契爾和康利雖然力圖追分，但太陽總能馬上回應。康利讀秒階段上籃得手，布克兩罰一中，再次留給
    爵士追平機會。米契爾造成犯規，可惜兩罰一中，保羅隨後用兩罰鎖定勝利。米契爾狂轟41分8籃板3助
    攻，本季單場得分次高；戈貝爾16分18籃板3抄截，波格丹諾維奇20分。康利拿到11分4助攻，克拉克森
    11分，兩人合計28投僅9中。爵士的三分攻勢難以有效施展，全場44投僅11中。"""