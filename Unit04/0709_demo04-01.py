#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# 加入測試文本的demo04-01.py

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

    baseballSTR = """本週三在紐約的比賽中，馬林魚此戰使用投手車輪戰，4名投手輪番上陣壓制大都會打線，前8局僅被敲出4支安打失1分，
    讓球隊能帶著2-1的領先優勢進入到9局下半。不過馬林魚推出巴斯登板關門，他面對首名打者麥尼爾，就被打出一發陽春砲，
    讓大都會追平比數，接下來又分別被敲出2支安打、投出保送，形成滿壘局面，此時輪到康福托上場打擊。在2好1壞的局面下，
    巴斯投了一顆內角滑球，康福托眼看這顆球越來越靠近自己的身體，似乎有下意識地將手伸進好球帶內，結果這球就直接碰觸到
    他的身肘，隨後主審庫爾帕判定這是一記觸身球，讓大都會兵不血刃拿下再見分，最終贏得比賽勝利。""".replace(" ", "").replace("\n", "")

    basketballSTR = """昨晚的紐約西區霸王之戰中，錯失勝利的太陽沒有就此束手就擒，延長賽一開始就打出7比2攻勢，米契爾和康利雖然力圖追分，
    但太陽總能馬上回應。康利讀秒階段上籃得手，布克兩罰一中，再次留給爵士追平機會。米契爾造成犯規，可惜兩罰一中，
    保羅隨後用兩罰鎖定勝利。米契爾狂轟41分8籃板3助攻，本季單場得分次高；戈貝爾16分18籃板3抄截，波格丹諾維奇20分。
    康利拿到11分4助攻，克拉克森11分，兩人合計28投僅9中。爵士的三分攻勢難以有效施展，全場44投僅11中。""".replace(" ", "").replace("\n", "")

    # 將 KNOWLEDGE_NBA_Teams.json 和 KNOWLEDGE_MLB_Teams.json 兩個體育類的字典讀取出來，合併成 mixedDICT 以後，寫入 mixedDICT.json 檔
    with open("ArticutAPI-master/Public_UserDefinedDict/KNOWLEDGE_NBA_Teams.json", encoding="utf-8") as f:
        nbaDICT = json.loads(f.read())
    with open("ArticutAPI-master/Public_UserDefinedDict/KNOWLEDGE_MLB_Teams.json", encoding="utf-8") as f:
        mlbDICT = json.loads(f.read())

    mixedDICT = {**nbaDICT, **mlbDICT}
    with open("mixedDICT.json", mode="w", encoding="utf-8") as f:
        json.dump(mixedDICT, f, ensure_ascii=False)

    # 將 baseballSTR 和 basketballSTR 兩篇文本各自送入 articut.parse() 裡，同時指定 userDefinedDictFILE 為剛才產生的 mixedDICT.json
    baseballResultDICT = articut.parse(baseballSTR, userDefinedDictFILE="./mixedDICT.json")
    basketballResultDICT = articut.parse(basketballSTR, userDefinedDictFILE="./mixedDICT.json")

    # 取得「動詞」做為特徵列表
    baseballVerbLIST = articut.getVerbStemLIST(baseballResultDICT)
    print("棒球文本動詞：")
    print(wordExtractor(baseballVerbLIST, unify=False))
    print("\n")
    print("籃球文本動詞：")
    basketballVerbLIST = articut.getVerbStemLIST(basketballResultDICT)
    print(wordExtractor(basketballVerbLIST, unify=False))
    print("\n")


    # 未知類別的文本
    unknownSTR01 = """金鶯隊左投John Means今天在面對水手隊比賽中，完成一項大紀錄，那就是以27個出局數，
    在沒有保送、觸身球、失誤的狀況下完成無安打比賽，而John Means差一點就有完全比賽，主要是3局下對Sam Haggerty
    投出不死三振，差點就可以完成「完全比賽」，金鶯最終以6:0贏球。根據紀錄，金鶯隊上次左投投出無安打比賽已經是1969年，
    也是大聯盟本季第三場無安打比賽，球隊史上第10位投出無安打比賽的投手，而他也是第一位在沒有投出保送、安打、失誤，
    卻投出無安打比賽的投手。""".replace(" ", "").replace("\n", "")

    unknownSTR01 = """米德頓再次證明公鹿不只有1名球星可以接管比賽！昨在東區冠軍賽G3，米德頓攻下追平季後賽生涯
    最高38分，其中末節包辦20分，帶領公鹿113比102逆轉擊潰地主老鷹，在東區冠軍賽取得2勝1敗領先優勢。「米德頓今天
    的表現太不真實了，」昨拿33分、11籃板及4助攻的「字母哥」阿提托康波表示，「他太不可思議了，在比賽尾聲帶領全隊
    前進，我今天所看到的他太偉大了，就是這麼簡單。」波提斯替補貢獻15分。谷底反彈 米德頓超感激。在前2場東區冠軍賽，
    米德頓表現不算理想，不僅平均只拿15分，投籃命中率也僅3成33（投36中12），三分命中率更低到1成25（投16中2），
    卻在昨天徹底谷底反彈，全場投26中15，含三分球投12中6。「我只是總算把那些球投進，」米德頓表示，「我有段時間陷
    入沒法把球投進的低潮，對我而言，今晚是把那些球開始投進的正確時機，對此我很感激。」公鹿總教練布登豪瑟也說：
    「我只是很開心他是我們的球員。」誤踩裁判 崔楊扭傷腳踝。除了米德頓末節狂掃20分，這場比賽的勝負關鍵更在第3節還
    剩29秒，老鷹後衛崔楊不慎踩到場邊裁判的腳，造成他右腳踝扭傷倒地，只能進入休息室治療，儘管他在末節仍回場上續打，
    進攻狀態已經不如先前。崔楊今天將接受核磁共振檢查，才知道他的腳踝傷勢嚴重程度，他昨天攻下老鷹全隊最高35分，
    卻在末節回到場上之後只拿3分，讓他不禁坦承，「真的很痛苦，真的很沮喪！我的腳踝傷勢確實讓我的速度都沒了。」
    「是的，我就是踩到那傢伙的腳上，我當時沒看到他，」崔楊說，「真的很倒楣，我所有傷痛都是踩到別人的腳，這是我
    不得不面對的艱難局面，但我想我必須腦後長眼才能看到裁判的腳。」G4明天續在亞特蘭大進行。""".replace(" ", "").replace("\n", "")

    unknownSTR01 = """就在罰球決定勝負的重要時刻，保羅很清楚該怎麼做！戴文布克昨天雖拿全場最高25分，
    卻在末節提前犯滿畢業，幸好太陽仍靠保羅讀秒階段6罰5中，驚險以84比80擊沉地主快艇，取得西區冠軍賽3勝1敗
    聽牌優勢。明回主場 盼隔28年再闖決賽「我始終告誡自己兒子，關於把球罰進的重要性。」昨拿18分、7助攻與4籃板
    的保羅表示，「假如連我自己都沒辦法做到，我憑什麼去要求兒子在罰球時保持專注。」艾頓也有19分，外加季後賽生涯
    新高22籃板。只要太陽明天回到鳳凰城主場贏下西區冠軍賽G5，就可相隔28年再次闖進總冠軍賽，昨在下半場氣到把面具
    摘下、無視鼻樑傷勢的戴文布克說：「我們現在還沒想到那麼遠！」布克全場投22中8，含三分球投5中0。如同保羅賽後所
    說，「這是一場充滿激情的瘋狂比賽！」趁著快艇上半場手感低迷，太陽一度領先到16分，快艇卻從第3節開始找回準星，
    轉眼縮小差距到1分，可惜就算滿場洛城球迷拚命加油，快艇就是無法超前。非進攻至上 兩隊命中率皆低。尤其來到讀秒階段，
    擁有3分領先的太陽，就是不給快艇三分追平機會，寧願故意把對方送上罰球線，就算保羅喬治、庫辛斯先後利用第2罰故意
    不進，企圖爭搶進攻籃板製造再攻機會，太陽仍靠保羅罰球穩住勝局。攤開兩隊比賽投籃數據，快艇全場投83中27，
    命中率僅3成25，太陽投86中31，命中率3成60，只比快艇稍微好一點，不過例行賽三分命中率位居聯盟最佳的快艇，
    全場竟然只投進5顆三分球，太陽也只進4顆。太陽總教練蒙提威廉斯說：「那就像揮拳互毆一樣，完全不是進攻至上，
    這點我可保證。」快艇總教練泰隆盧也無奈表示，「我們至少擁有12次可以超前的機會，卻始終沒法做到，那些我們該進的球都沒投進。」""".replace(" ", "").replace("\n", "")


    unknownSTR01 = """這次老鷹再怎麼抱怨「字母哥」阿提托康波罰球違例也沒用了！公鹿26日在東區冠軍賽G2第2節打出
    誇張20比0凶猛攻勢，甚至數度領先到40分以上，最後以125比91轟翻老鷹，也把東區冠軍賽扳成1平，字母哥貢獻全場最高25分，
    外加9籃板、6助攻。雙方打完首節，地主公鹿僅以34比28領先，沒想到老鷹次節完全崩盤，從崔楊在上半場還剩6分25秒投進兩分球
    之後，整整快5分鐘進入得分乾旱期，且失誤連連，讓公鹿打出誇張20比0猛攻，轉眼就把領先差距擴大到30分以上。上半場結束，
    公鹿取得77比45大幅領先，比賽勝負幾乎提前底定，公鹿半場就有3人得分上雙，哈勒戴19分最高，阿提托康波17分、7籃板及5助攻，
    布魯克羅培茲13分，公鹿上半場命中率6成33，第2節更轟43分，老鷹僅17分。來到下半場，公鹿仍沒打算給作客的老鷹任何反撲機會，
    打完前3節，公鹿取得103比63遙遙領先，老鷹不僅早早就讓崔楊坐在場邊休息，末節更派板凳球員上場，擺明就當垃圾時間在打，
    畢竟接下來東區冠軍賽G3將回亞特蘭大進行。除了阿提托康波全能演出，哈勒戴也幫公鹿貢獻22分、7助攻，前役手感低迷的米德頓，
    則有15分、8助攻與7籃板，布魯克羅培茲16分；老鷹以崔楊15分最高，只是跟他在G1狂掃48分的瘋狂火力相比，老鷹會輸這麼慘並不意外。 """.replace(" ", "").replace("\n", "")

    unknownSTR01 = """這次保羅喬治沒讓滿場洛杉磯球迷失望！喬治昨在西區冠軍賽G3貢獻全場最高27分，
    且在第3節領軍打出誇張21比3猛攻，幫助快艇106比92力挫迎回保羅的太陽，除了拒絕太陽提前聽牌，
    也終止太陽季後賽9連勝。由於里歐納德右膝扭傷持續缺陣，保羅喬治扛下快艇一哥責任，面對前役關鍵時間兩罰落空窘境，他昨天除拿全場
    最高得分，更有15籃板、8助攻，罰球也回歸穩定的罰7中6，重新展現「Playoff P」應有風貌。不想被聽牌 快艇展現韌性。「我知道必須
    變得更好，」保羅喬治表示，「我的所有能量都帶領我走向更棒比賽。」快艇今年季後賽連3輪都面臨0勝2敗窘境，前兩輪卻成功逆轉擊退
    獨行俠與爵士，如今到了西區冠軍賽當然也想比照辦理。替快艇貢獻23分的雷吉傑克生表示，「我們持續擺脫低潮，
    且試著找出方法讓我們變得更好，更跟對手展現我們的韌性，我們不僅展現心臟強度，也跟對手拚戰到底。」
    快艇中鋒祖巴茲15分、16籃板，曼恩12分。自從16日驚傳感染新冠病毒，保羅缺席了前兩場西區冠軍賽，
    昨天復出就回前東家快艇主場，更在球員介紹時遭到球迷狂噓，最後雖有15分、12助攻，全場投19中5卻很不理想，
    沒想到戴上面具的戴文布克更慘。太陽CP3復出 戴文布克啞火。前役遭到貝弗利額頭猛撞，戴文布克鼻梁出現3處骨裂，
    讓他只能戴上面具，這嚴重影響到他的手感，全場出手21次只進5球，更麻煩的是，前兩戰頂替保羅上場表現優異的佩恩，
    只打5分鐘就扭傷左腳踝退場。太陽總教練蒙提威廉斯賽後強調，自己不該讓保羅打了那麼久時間（39分鐘），「保羅或許很累，
    但當佩恩傷退且沒法回來，這對我們很傷，所以我讓保羅打得比較久，責任都在我身上。」艾頓攻下太陽最高18分。""".replace(" ", "").replace("\n", "")

    unknownSTR01 = """雖然少了主力球星里歐納德，但快艇還有二當家保羅喬治，昨在背水一戰的下半場狂砍30分，
    全場41分、13籃板、6助攻、3抄截，幫助洛杉磯116比102射落太陽，西區決賽2比3逆天續命。馬可斯莫里斯首節6投
    全中攻下13分，快艇取得10分領先優勢，第4節太陽趁著保羅喬治不在場上的時候逆轉超前，雷吉傑克生飆進2顆三分球，
    緊接著又單手暴扣，率領球隊再次超前，奠定了勝利基礎。上半場讓隊友表演的保羅喬治，下半場戰神附體，全場20投
    15中，包含了3顆三分球，攻下個人季後賽生涯新高41分，成為快艇能夠保有一線生機的最大功臣。保羅是快艇隊史季
    後賽第一位單場攻下40分、13籃板、6助攻的球員，第3節獨拿20分追平隊史紀錄，也是NBA史上第4位季後賽連續18場
    得分超過20分的球員，其他3位分別是杜蘭特、布萊恩以及喬丹大帝。此外，保羅喬治還是自1996-97賽季之後，NBA
    第3位在季後賽下半場得到超過30分且投籃命中率不低於80%的球員，前兩位球員分別是2010年的韋德與2020年的安東尼戴維斯。
    保羅喬治同時也是NBA史上首位在季後賽單場得分超過40分，投籃命中率高達75%、三分命中率50%、罰球命中率100%的球員。
    快艇教頭泰隆盧率挺球隊本季第7次在系列賽落後時獲勝，創造了NBA紀錄。泰隆盧在季後賽面臨被淘汰的時候執教生涯戰績10勝2敗。
    除了保羅喬治外，雷吉傑克生貢獻23分，馬可斯莫里斯挹注22分，兩人上下半場的左右鉤拳打得太陽顧此失彼。莫里斯16投9中，
    投籃命中率超過50%的時候快艇8戰全勝。""".replace(" ", "").replace("\n", "")

    unknownSTR01 = """季後賽太陽更是打出強悍實力，首輪4比2淘汰由詹姆斯率領的衛冕軍湖人，次輪直落4橫掃例行賽MVP
    約基奇坐鎮的金塊。西區決賽保羅雖因觸碰到防疫規定導致被隔離，仍有戴文布克、艾頓與佩恩聯手，拿下季後賽9連勝，
    改寫隊史紀錄。此役高潮迭起，劇情一轉再轉，尤其是最後1分鐘雙方攻防堪稱經典之作，保羅喬治兩度幫助快艇超前，
    可惜最後8.2秒竟兩罰俱失，0.9秒太陽最後一擊，克勞德底線發球，戴文布克掩護成功，艾頓竄身至籃下躍起，將克勞德
    的空拋球灌進籃框內，憑藉這精采一灌，太陽得以上演驚天逆轉秀。太陽致勝功臣艾頓攻下24分、14籃板，季後賽場均
    投籃命中率高達72.3%，成為計時器時代（1954-55賽季）以來第一個在季後賽12場比賽投籃命中率超過70%的球員，
    也是太陽隊史第3位在季後賽最後1秒完成絕殺的球員，先前兩位分別是2003年的馬布瑞和2006年的迪奧。佩恩轟29分
    贏球大功臣。曾被NBA拋棄的佩恩，一度轉戰大陸CBA討生活，只打2場比賽就遭開除，這段難堪往事激勵了佩恩奮勇向上
    的決心，此役砍進全場最高29分、9助攻。""".replace(" ", "").replace("\n", "")


    unknownSTR01 = """大谷翔平29日生涯二度到洋基球場比賽，一局上首打席就轟出全壘打，生涯在洋基球場打出的第1支安打，
    飛行距離416英尺，擊球初速117.2英里，相當於188.6公里。30日三局上轟出右外野全壘打，五局上第三打席，在2好1壞的
    第5顆球，94英里直球，轟出右外野2分全壘打，連2打席開轟的單場雙響砲。大谷翔平生平第一次在洋基球場單場雙響砲，
    在洋基球場2場比賽已打出3支全壘打，本季第28轟、6月第13轟、近13戰第11轟。連2場全壘打秀之後，大谷翔平7月1日
    將要先發登板投球，這是大谷翔平第1次站上洋基球場的投手丘先發。天使隊總教練梅登表示，大谷翔平會自己上場打擊，
    取消指定打擊，唯一可以阻止大谷翔平先發投球又打擊的只有天氣太熱。""".replace(" ", "").replace("\n", "")


    unknownSTR01 = """火腿與樂天隊昨天以5：5和局收場，兩名台將各自有關鍵貢獻，王柏融在滿壘時敲出二壘打清壘，
    宋家豪則以10球完成第9局凍結比分的任務，送出兩次三振。王柏融此役擔任4棒、指定打擊，助燃火腿在第3局的4分大局，
    3安打先馳得點後，近藤健介獲得保送，王柏融在滿壘時打到中左外野警戒區落地，這支二壘打灌進3分打點，火腿取得4：0領先。
    王柏融狙擊143公里卡特球，一棒清光壘上隊友，他表示，「滿壘時的打擊，就是希望無論如何都要把隊友送回來，很開心出現最好的結果。」
    王柏融4打數敲出1安打、吞下2次三振，貢獻3分打點，而他本季在滿壘時頗有心得，累積7打數敲出3安打，掃回9分打點。
    火腿在第4局由渡邊諒補上陽春砲，一度5：0領先卻守不住，樂天先在4局下靠岡島豪郎的二壘打追回1分，5局灌進4分，
    洋聯打點王島内宏明的兩分打點二壘打，幫助樂天以5：5追平，兩隊接下來都沒有分數進帳。宋家豪在9局上登板，
    無緣與王柏融上演「台灣內戰」，雖遭石川亮敲出安打，但也僅用10球就完成1局無失分任務，送出2次三振，最快球速150公里，防禦率下修1.14。""".replace(" ", "").replace("\n", "")


    unknownSTR01 = """統一7-ELEVEn獅週末在台南主場二連戰，週日（16）賽事交手樂天桃猿，兩隊雖擊出不分軒輊8支安打，
    不過樂天串聯效率更勝一籌，終場5：0送給統一本季首度被完封比賽，也終止獅隊跨季連續90場得分。左手洋投飛利士生涯初登板
    表現不俗，只在第一局被林立、陳俊秀擊出安打失1分，很快漸入佳境，直到6局上才遭陳俊秀棒打陽春砲再掉分，7局僅被擊出4支
    安打掉兩分，送出5K，可惜好投無緣勝利，還吞下首敗。不過首戰表現，他認為有達到預期，各球路都投得不錯，10分滿分有8.5
    高分，總教練林岳平也覺得相當理想，有辦法攻擊打者內角。表現不俗還有樂天本土低肩側投黃子鵬，前兩戰對統一0勝2敗，
    防禦率5.73偏高，今天前段比賽投出5.1局無失分，6次奪三振壓制，他表示，第6局是自己面臨的課題，身為先發投手，
    想把局數拉長，分擔牛棚壓力，今天面對左打部隊，想法簡單一點，相信捕手照著策略投，拿下對戰1勝並終止近期3連敗低潮。
    飛利士退場後，樂天於9局上吃下3分大局，讓原本只有兩分落後的獅隊陷入苦戰，9局下陳禹勳續投，連取3出局結束比賽。
    此役擔任樂天第4棒陳俊秀猛打賞，挹注3分打點，獲選單場MVP，統一「雙傑」陳傑憲、蘇智傑雖也同樣猛打賞，
    但攻勢幾乎集中在兩人，欠缺適時一擊，仍遭完封命運。""".replace(" ", "").replace("\n", "")


    unknownSTR01 = """統一7-ELEVEn獅和富邦悍將在台南棒球場交手，雖然富邦一路領先，不過獅子軍展現韌性，
    九局下將比數追平，延長十局下新秀林子豪把握滿壘機會，擊出再見安打結束比賽，幫助球隊以3:2擊敗富邦，統一也達成隊史1700勝。
    富邦面對統一先發投手猛威爾，分別在三局、五局靠著串聯安打各攻下1分，且洋投邦威繳出精彩好投，7.2局只被擊出零星4安，
    飆出11K，徹底封鎖獅隊打線，眼看就要拿下勝利，守護神陳鴻文卻在九下失守。陳鴻文一出局後，連續保送蘇智傑、林子豪，
    雖三振姚雨翔取得第二個出局數，但被何恆佑、林岱安各敲出帶有1分打點的安打，讓球隊被統一扳平。比賽進入延長，
    陳韻文十局上主投1局送出2K無失分。十局下，富邦更換歐書誠接替投球，卻接連被陳傑憲、林安可打出安打攻占一三壘，
    教練團緊急再換上陳韋霖登板，選擇故意四壞保送蘇智傑，但面對林子豪仍被擊出左外野深遠飛球形成再見安打。
    林子豪這支再見安打為生涯首支，同時也以歲齡19歲又47天，刷新中華職棒最年輕擊出再見安打紀錄，賽後獲頒單場最有價值球員。
    猛威爾本場比賽投7局，被敲9安失2分，送出6K、3保送。劉軒荅、鄭鈞仁各中繼1局無失分，勝投由陳韻文拿下，敗投則由歐書誠承擔。""".replace(" ", "").replace("\n", "")

    unknownSTR01 = """中信兄弟先發投手余謙在開局就遇到亂流，被對方首名打者李凱威擊出安打上壘，演出盜壘成功，
    下一棒郭天信擊出飛球遭到接殺，同時跑者進佔三壘時遭到觸殺形成兩出局，眼看即將化解危機，卻保送陳品捷，
    再被劉基鴻、赫雷拉擊出安打送回2分，龍隊先馳得點。2局下，歐晉、蔣少宏雙雙擊出二壘安打再攻下1分，吳東融補上內野安打，
    郭天信同樣敲安再送回1分，也將余謙打退場，由王梓安接替投球。3局下，龍隊再有分數進帳，劉基鴻、赫雷拉分別遭到觸身球及
    四壞球保送，林驛騰擊出內野安打形成滿壘，歐晉雖擊出雙殺打，但味全跑回1分。接下來再靠投手暴投得1分，將比數拉開至6：0領先中信。
    4局下，李凱威擊出安打後再盜上二壘，劉基鴻補上安打再送回1分，比數來到7：0。6局下，面對中信第4任投手蔡齊哲，
    吳東融擊出三壘安打來到得分大門口，李凱威擊出帶有1分打點的高飛犧牲打，比分已拉至8分差距。7局下，中信投手吳俊偉保送林驛騰，
    蔣少宏、吳東融擊出連續安打，幫助球隊再拿下1分，味全以9：0大幅領先兄弟。對比龍隊打線單場擊出14支安打，中信兄弟僅在1局上
    由周思齊從伍鐸手中敲出全場唯一一支安打，打擊熄火種下敗因，終場中信兄弟就以0：9敗給最近火力兇猛的味全龍隊，也中止對戰四連勝，
    以0.558勝率暫居第二，僅次於0.564勝率的統一7-ELEVEn獅隊。此戰余謙僅投1.1局就被擊出7支安打，送出1保送，失掉4分自責分，
    防禦率飆升至7.56，吞下生涯首敗。伍鐸主投6局僅被敲出1支安打，送出1K無失分，優質先發表現不僅拿下本季第3勝，也帶領球隊奪下5連勝，賽後獲選單場MVP。""".replace(" ", "").replace("\n", "")

    unknownSTR01 = """因應疫情升溫，中華職棒自今(12)日起採取閉門比賽，在無觀眾的台南棒球場，
    中信兄弟和統一7-ELEVEn獅進行本週第二場對戰，地主統一在先發投手布雷克繳出7局無失分好投帶領下，終場以4:1擊敗中信，
    將兩隊勝差再度拉近至0.5場。面對中信先發投手陳琥，獅隊打者在一局下半就展開攻勢，蘇智傑獲得四壞保送後盜上二壘，
    下一棒郭阜林隨即敲安幫助球隊首開紀錄，統一取得1:0領先。三局下半，獅子軍攻勢再起，首棒打者陳傑憲從陳琥手中擊出個人本季第1轟，
    接著連續3棒打出安打，也逼著中信教練團緊急換上官大元中繼登板，才拿到這個半局的3個出局數，不過統一8個人次的猛攻，仍將比數拉開至4:0。
    總計陳琥今日僅投了2局，被敲5安失4分皆為自責分，吞下本季首敗，防禦率飆高至雙位數來到11.12。接替上場的官大元，
    中繼3局無失分，目前防禦率仍是完美的零，王奕凱、謝榮豪各負擔1局和2局的投球任務也都無失分。布雷克本場比賽7局的投球，
    只被擊出6安，送出5K、2BB，沒有任何失分，拿下本季第6勝，賽後也獲頒單場最有價值球員。江承峰第8局登板，被敲2安加上守備失誤掉1分非自責分，
    而這也是中信兄弟今日唯一的得分。九局上，由守護神陳韻文上場關門，送出2張老K，為球隊守住勝利，入帳本季第11次救援成功。""".replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownVerbLIST = articut.getVerbStemLIST(unknownResultDICT)
    print("未知文本動詞：")
    print(wordExtractor(unknownVerbLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個動詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballVerbLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballVerbLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownVerbLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[棒球文本 vs. 未知文本] 的動詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[籃球文本 vs. 未知文本] 的動詞餘弦相似度:{}".format(basketball2unknownSIM))


    # 取得「名詞」做為特徵列表
    baseballNounLIST = articut.getNounStemLIST(baseballResultDICT)
    print("棒球文本名詞：")
    print(wordExtractor(baseballNounLIST, unify=False))
    print("\n")
    print("籃球文本名詞：")
    basketballNounLIST = articut.getNounStemLIST(basketballResultDICT)
    print(wordExtractor(basketballNounLIST, unify=False))
    print("\n")



    # 未知類別的文本
    unknownSTR01 = """金鶯隊左投John Means今天在面對水手隊比賽中，完成一項大紀錄，那就是以27個出局數，
    在沒有保送、觸身球、失誤的狀況下完成無安打比賽，而John Means差一點就有完全比賽，主要是3局下對Sam Haggerty
    投出不死三振，差點就可以完成「完全比賽」，金鶯最終以6:0贏球。根據紀錄，金鶯隊上次左投投出無安打比賽已經是1969年，
    也是大聯盟本季第三場無安打比賽，球隊史上第10位投出無安打比賽的投手，而他也是第一位在沒有投出保送、安打、失誤，
    卻投出無安打比賽的投手。""".replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownNounLIST = articut.getNounStemLIST(unknownResultDICT)
    print("未知文本名詞：")
    print(wordExtractor(unknownNounLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個名詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballNounLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballNounLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownNounLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[棒球文本 vs. 未知文本] 的名詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[籃球文本 vs. 未知文本] 的名詞餘弦相似度:{}".format(basketball2unknownSIM))




    # 取得「TF-IDF」做為特徵列表
    baseballTFIDFLIST = articut.analyse.extract_tags(baseballResultDICT)
    print("棒球文本 TF-IDF：")
    print(baseballTFIDFLIST)
    print("\n")
    print("籃球文本 TF-IDF：")
    basketballTFIDFLIST = articut.analyse.extract_tags(basketballResultDICT)
    print(basketballTFIDFLIST)
    print("\n")



    # 未知類別的文本
    unknownSTR01 = """金鶯隊左投John Means今天在面對水手隊比賽中，完成一項大紀錄，那就是以27個出局數，
    在沒有保送、觸身球、失誤的狀況下完成無安打比賽，而John Means差一點就有完全比賽，主要是3局下對Sam Haggerty
    投出不死三振，差點就可以完成「完全比賽」，金鶯最終以6:0贏球。根據紀錄，金鶯隊上次左投投出無安打比賽已經是1969年，
    也是大聯盟本季第三場無安打比賽，球隊史上第10位投出無安打比賽的投手，而他也是第一位在沒有投出保送、安打、失誤，
    卻投出無安打比賽的投手。""".replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownTFIDFLIST = articut.analyse.extract_tags(unknownResultDICT)
    print("未知文本 TF-IDF：")
    print(unknownTFIDFLIST)
    print("\n")


    # 利用 Counter() 模組計算每個 TF-IDF 特徵詞出現的次數
    baseballCOUNT = Counter(baseballTFIDFLIST)
    basketballCOUNT = Counter(basketballTFIDFLIST)
    unknownCOUNT = Counter(unknownTFIDFLIST)

    # 計算 [棒球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；計算 [籃球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[棒球文本 vs. 未知文本] 的 TF-IDF 特徵詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[籃球文本 vs. 未知文本] 的 TF-IDF 特徵詞餘弦相似度:{}".format(basketball2unknownSIM))

    # ############################################
    # ####
    # 未知類別的文本
    unknownSTR02 = """保羅（Chris Paul）今日面對騎士再度展現他的「零失誤」功力，整場比賽打了36分鐘，拿到23分16助攻6籃板4抄截2阻攻，
    沒有出現1次失誤，這是他今年賽季第10次單場0失誤表現。根據統計，這是保羅生涯第3度至少拿到20分15助攻外加0失誤，自從1977-78年開始統計
    失誤以來，只有奈許（Steve Nash）和保羅曾3度達此高標。此外，保羅生涯共44次以0失誤表現達成助攻雙位數，在聯盟歷史上僅次於伯格斯
    （Muggsy Bogues）的46次。 """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR02, userDefinedDictFILE="./mixedDICT.json")
    unknownVerbLIST = articut.getVerbStemLIST(unknownResultDICT)
    print("未知文本動詞：")
    print(wordExtractor(unknownVerbLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個動詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballVerbLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballVerbLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownVerbLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[棒球文本 vs. 未知文本] 的動詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[籃球文本 vs. 未知文本] 的動詞餘弦相似度:{}".format(basketball2unknownSIM))





    # 取得「名詞」做為特徵列表
    baseballNounLIST = articut.getNounStemLIST(baseballResultDICT)
    print("棒球文本名詞：")
    print(wordExtractor(baseballNounLIST, unify=False))
    print("\n")
    print("籃球文本名詞：")
    basketballNounLIST = articut.getNounStemLIST(basketballResultDICT)
    print(wordExtractor(basketballNounLIST, unify=False))
    print("\n")



    # 未知類別的文本
    unknownSTR02 = """保羅（Chris Paul）今日面對騎士再度展現他的「零失誤」功力，整場比賽打了36分鐘，拿到23分16助攻6籃板4抄截2阻攻，
    沒有出現1次失誤，這是他今年賽季第10次單場0失誤表現。根據統計，這是保羅生涯第3度至少拿到20分15助攻外加0失誤，自從1977-78年開始統計
    失誤以來，只有奈許（Steve Nash）和保羅曾3度達此高標。此外，保羅生涯共44次以0失誤表現達成助攻雙位數，在聯盟歷史上僅次於伯格斯
    （Muggsy Bogues）的46次。 """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR02, userDefinedDictFILE="./mixedDICT.json")
    unknownNounLIST = articut.getNounStemLIST(unknownResultDICT)
    print("未知文本名詞：")
    print(wordExtractor(unknownNounLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個動詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballNounLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballNounLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownNounLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[棒球文本 vs. 未知文本] 的名詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[籃球文本 vs. 未知文本] 的名詞餘弦相似度:{}".format(basketball2unknownSIM))




    # 取得「TF-IDF 特徵詞」做為特徵列表
    baseballTFIDFLIST = articut.analyse.extract_tags(baseballResultDICT)
    print("棒球文本 TF-IDF：")
    print(baseballTFIDFLIST)
    print("\n")
    print("籃球文本 TF-IDF：")
    basketballTFIDFLIST = articut.analyse.extract_tags(basketballResultDICT)
    print(basketballTFIDFLIST)
    print("\n")



    # 未知類別的文本
    unknownSTR02 = """保羅（Chris Paul）今日面對騎士再度展現他的「零失誤」功力，整場比賽打了36分鐘，拿到23分16助攻6籃板4抄截2阻攻，
    沒有出現1次失誤，這是他今年賽季第10次單場0失誤表現。根據統計，這是保羅生涯第3度至少拿到20分15助攻外加0失誤，自從1977-78年開始統計
    失誤以來，只有奈許（Steve Nash）和保羅曾3度達此高標。此外，保羅生涯共44次以0失誤表現達成助攻雙位數，在聯盟歷史上僅次於伯格斯
    （Muggsy Bogues）的46次。 """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR02, userDefinedDictFILE="./mixedDICT.json")
    unknownTFIDFLIST = articut.analyse.extract_tags(unknownResultDICT)
    print("未知文本 TF-IDF：")
    print(unknownTFIDFLIST)
    print("\n")


    # 利用 Counter() 模組計算每個 TF-IDF 特徵詞出現的次數
    baseballCOUNT = Counter(baseballTFIDFLIST)
    basketballCOUNT = Counter(basketballTFIDFLIST)
    unknownCOUNT = Counter(unknownTFIDFLIST)

    # 計算 [棒球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；計算 [籃球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[棒球文本 vs. 未知文本] 的 TF-IDF 特徵詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[籃球文本 vs. 未知文本] 的 TF-IDF 特徵詞餘弦相似度:{}".format(basketball2unknownSIM))