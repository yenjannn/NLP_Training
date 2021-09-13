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


    baseballSTR = """今天是108學年度的畢業典禮。我很高興能和所有師長們一起，向畢業同學們表達誠摯的祝福。我們也祝賀在場與不在場的家長們，恭喜大家終於可以放下一樁心事了。今年，我們一起經歷了一個非常不一樣的春天。當WHO在五個月前宣布發現新型病毒時，甚至在1月21日台灣出現第一個確診病例時，絕大多數人都不曾想到，一場即將席捲全球的傳染病已經迫在眉睫。隨著疫情發展，我們的開學日被推遲了，校園的活動與進出受到許多限制，課程也紛紛轉為遠距線上教學。即使目前國內疫情已趨和緩，我們還是得遵循防疫規定，縮小畢業典禮的規模；對於無法到場參與畢業典禮的同學，家長和師長們，我們衷心感到抱歉。
    在這段特殊時期，校內所有同仁都積極投入防疫工作。我們安置了大批需要居家檢疫的同學，啟動了海外同學的安心就學方案，也妥善布置各館舍與校園的防疫管制。此外，老師們準備遠距教學，同學們也都能全力配合防疫措施。我們校園至今沒有出現防疫缺口，教學、研究和行政都井然有序的進行；這是所有台大人共同努力的結果。不僅如此，許多老師積極參與政府的防疫工作，投入病毒快篩和疫苗的研發；還有同仁發展了新的防疫設備，如防疫一號，而且開放給社會自由使用。我很高興看到，我們展現了一個在困難時期仍然緊密團結並且與社會共同抗疫的台大。大家一定注意到，這場疫情已經開始改變我們的行為模式與社會形態。許多產業受到衝擊，特別是需要面對面接觸的行業；而未來，遠距上班和遠距學習將成為新常態。我以前總在不同演講，包括去年的畢業典禮，提醒大家，這個世界正以驚人的速度改變。如今疫情讓許多預期的改變成為現實，而這正是大家畢業後將要面對的新世界。面對後疫情時代，我有兩點想法提供給大家參考。當我們戴上口罩，避免與其他人接觸時，我們也正在拉開人與人之間的距離，甚至區域與區域之間的距離。而實體距離帶來心理疏離，也引發更多猜忌和不安。在這個時刻，我希望大家不要忘記關心他人，關懷社會，並且永保這樣的熱情。藉由這些關心與關懷縮短彼此間的心理距離，讓我們的社會仍能緊密連結。將第一個想法擴充與深化，是我想講的第二點。由於當前國際，如中美之間呈現相互對抗的情勢，各國也因疫情而紛紛封閉邊境，許多人認為，這或許將使延續近30年的全球化浪潮，至此畫下句點。但我的想法不是如此。我認為，在資訊科技的推動下，全球化這個趨勢不會改變。國際秩序可能重組，國際經濟重心可能移動，這些調整將改變全球化的樣貌，卻不會阻止全球化繼續發展。換言之，各位同學畢業後，仍將面對全球化的挑戰。
    這就回到了老生常談的議題：對於全球化我們該有什麼樣的準備？「關鍵評論」五年前一篇文章，作者為 Yixian，有段怵目驚心的話：「台灣人對於這個世界沒有什麼概念，對於種族也一概不知，對歧視一點都不敏感。但我們歧視起人來一點都不手軟。」歧視的根本原因在於缺乏對不同種族，宗教，性別等所有人的關懷，以及對各種文化的理解尊重。作者於是強調，除了除了IQ與EQ之外，我們還需要重視文化智商（cultural quotient，簡稱CQ）。CQ衡量的是對於不同文化的理解能力，以及相互接納適應的能力。面對全球化趨勢，我們該重視的不僅是工具性的「說好外語」或技術面的「國際競爭力」而已，還要具備欣賞不同文化，與不同文化自然相處，水乳交融的能力。唯有這樣，我們才能在全球化中找到自己的位置，乃至成為引領趨勢的人。在大家即將畢業的時刻，我謹以「常保熱情關懷，培養文化智商」這兩句送給所有畢業同學。再次祝福大家，並且期待再見。謝謝。
    """.replace(" ", "").replace("\n", "")

    basketballSTR = """今天我很高興來到這裡，並想告訴你們一些我的經歷。今天也將是你們走向生活挑戰的開始。現在，機會的大門正在向你們打開，多麼鼓舞人心。德國作家黑塞（Hermann Hesse）對這種情況有一些美妙的描述：「所有的開始都擁有神奇的力量，護衛和幫助我們的生活。」當24歲的我拿到物理學位的時候，這首詩啟發過我。那是1979年，世界被分成了東、西兩大陣營，處於冷戰階段。畢業工作後，我每天下班走過柏林圍牆，那是一道鋼筋水泥障礙，阻隔城市、人民和家人，包含我自己的家人。我不是異見者，也沒有衝撞過那堵牆。但是，我也從來無法否認那堵牆就在那裡。我不想自己欺騙自己。柏林圍牆囿限了我的機會，它真真實實的擋住了我的去路。但它存在的那些年，卻也有做不到的事：它無法囿限我的思想、我的性格、我的想像力、夢想和渴望。1989年，自由浪潮席捲歐洲。從波蘭到匈牙利、捷克斯洛伐克，還有東德，成千上萬的人勇敢地湧上街頭。人民的力量，推翻了柏林牆！我親身經歷過動彈不得、無從改變的景況。親愛的畢業生們，這是我想與你們分享的第一個經驗：任何看似如磐石、亙古不變的事，事實上都可以改變。
    不久之後，我們這一代的政治家將退出歷史舞台，你們是將我們帶到未來的一代人。保護主義、貿易衝突，危及國際自由貿易，讓我們的繁榮基礎漸漸流失。數位資訊革命從各層面影響我們生活。戰爭和恐怖主義導致人們流離失所。氣候變化對地球的自然資源構成威脅，而人類需要對這個危機以及更多的後果負責。我們要能夠、也必須盡一切可能，應對這一挑戰。現在行動還來得及，但是需要我們每個人都發揮作用。比起過往任何時刻，現在的我們更需要多邊合作，而非單邊行動；要全球性思考，而非國家思考；要對外開放，而不是孤立主義。簡單的說，我們必須牽起手，而不是孤軍奮戰。親愛的畢業生們，你們將來會有比我們這一代人更多的機會。畢竟，光你們的智慧手機，就可能比蘇聯製造的IBM主機電腦，具有更多的應用能力。例如，現今我們可以用人工智慧，從數百萬張影像裡找出病徵，用於更好地診斷癌症（等疾病）。將來，一個充滿洞察力的機器人，就可能幫助醫生和護士關注病患個性化需求。
    2019年畢業生們，你們將很大程度地決定我們在未來如何利用這些科技。請思考我們是在制定科技規則，還是科技把我們牽著鼻子走？我們是否充分優先考慮人的尊嚴，還是只是將大眾當成消費者、大數據來源，甚至是觀察監控對象？這些都是具有挑戰的問題。我的經驗是，如果我們習慣換位思考，就可以找到很好的答案。這還包括，我們能尊重他人的歷史、傳統、宗教和身份，堅守自己的價值觀並保持一致，在緊迫之下，也能不衝動行事且保持深思熟慮來做決策。當然，這肯定需要勇氣。重要的是，我們需要對他人以誠相待。也許最重要的，我們首先要能誠實地面對自己。然而，親愛的畢業生，有什麼可能阻止你們？阻止我們實現這些？答案是，牆。人們心中的牆，無知的牆壁和狹隘的思想。它們存在於家人之間，也存在於社會中不同膚色、民族和宗教的群體之間。牆不斷阻止我們對世界協調合作的設想。我們是否能做到這一點，取決於我們自己。沒有什麼是理所當然的。個人自由不是從天而降的，民主制度也並非理所當然地一直健全存在。同樣，人類的和平和繁榮都不是必然的。當你走出去的那一刻，也是冒險開始的時刻。學會繼往開來。任何的開始都有結束的時候，白天始終有黑夜相隨，生命都逃避不了死亡。但是，如果我們打破桎梏自己的牆壁，如果我們擁抱開放並有勇氣步入新的開始，一切皆有可能。我們的一生會遇到各種不同。開始和結束之間，有著空間。我們稱之為生命和經驗。我一直相信，我們需要做好準備，習慣結束。因為這是新起點的啟航，這樣能幫助我們充分把握未來的機會。這是我無論做學生，做科研，還是從政後，不斷體會的道理。誰知道在我離任之後，將會有什麼樣的生活。但是，一定也會是追求新的挑戰的生活。有一件事是很清楚的，將再次是不同的新生活。這就是為什麼我要把這個希望留給你們，推倒無知和狹隘的牆，因為沒有什麼必須保持原樣。
    """.replace(" ", "").replace("\n", "")

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
    print("台大：")
    print(wordExtractor(baseballVerbLIST, unify=False))
    print("\n")
    print("梅克爾：")
    basketballVerbLIST = articut.getVerbStemLIST(basketballResultDICT)
    print(wordExtractor(basketballVerbLIST, unify=False))
    print("\n")


    # 未知類別的文本 (清大)

    unknownSTR01 = """恭喜畢業生完成了大學的學業，誠如人們所說的，Commencement正是一個新的開始。今天以後，在各位面前的旅程正要展開，包括知識的旅程、人生的旅程，都將瑰麗多彩，令人期待。西元1231年當時80歲的巴黎大學只有四個系：神學/醫學/法學/藝術，這也是西方世界數百年的高等教育知識範疇。隨著文藝復興和大學的社會化，直到近兩百年前，人文與社會科學、自然科學與工程加入高等教育的內容之中，直到今天，大家所學習的知識，大體上在這個系統之中。然而各位畢業所面臨的，是科技和全球化進一步爆發的世界，知識以前所未有的速度增長並且唾手可得，兩百年前定義的知識軌道，或者今天所說的一技之長，很難可以在人生的旅程一帆風順收穫豐富。
    尋找知識旅程的藍海，往往是在兩三個既有知識範疇之間，穿越山峽而出，豁然開朗；又或者是在另一座知識的山岳上，看明白原先所來之處蜀道難行的前山後水，因此而看見新的攀越隘口。許多新的產業、新的機會，例如大數據、例如金融工程、例如物聯網、例如虛擬實境，都不能在單獨一個兩百年前的知識範疇所掌握，而極為需要兩個以上的既有知識領域互相匹配補充。如同水陸交匯之地，常常可以發現最為豐富的生態物種。未來全球一家所面臨的重大問題，例如環境與永續、例如移民與文化、例如能源、例如高齡化社會，都需要跨越大範圍的多種知識整合起來尋求答案。當世界上對人才的描述，從I字進而為T字再進而為π字的型態，我們可以清楚看到單一領域專長在未來的侷限。大學的學習，是弱水三千取一瓢飲，使大家熟悉進入一個知識領域的必經歷程，未來在其他的知識旅程可以模仿或者對照。在這裡我也特別要恭喜大家當中，完成了双專長學習的同學，你們在辛勤之中獲得了更豐富的知識旅程經驗。清華每一屆畢業生已經有20%擁有双專長，這在國內各大學是非常難得的。進入社會之後我們所面臨的工作場域，除了專業知識，經常更被重視的是對於不同專業背景之間的理解溝通能力，對於人與社會的了解與應對。專業知識可以在大學裡經由設計好的學程「學而知之」而得到，後者則往往是在工作的需求之中「困而知之」，要靠大家保持不斷虛心學習的動機而得到。如同將官不分兵科，如果要將自己的能力做更大的發揮，為人群做更大的貢獻，跨出自己從大學畢業當時的單一領域，是絶對必要的。期待清華人，未來除了知識旅程的跨越加成，在人生的旅程上，能勇敢跨出自己畢業時的人生經驗，有意識地去探索去接納不同地域、不同年齡、不同種族、不同社經背景的人，學習他們的人生經驗，培養自己更大的能力和心量，去組合去歸納更高層次的人生價值與所追求的目標。每一個清華人的人生風格可以不同，人生旅程的風景一定互異，但是所追求的旅程目標應當要高要遠。清華的教育在於培養君子，君子或者狂或者狷，但是君子不器，不侷限在一個知識領域，不侷限在一個地域、一個年紀、一個種族、一個社經出身的視角。這是今天在各位的畢業典禮上，希望對大家說說有關於「君子不器 突破自我 跨越領域」的話。自今以後，各位或許不會經常聽到看到校訓「自強不息 厚德載物」，但希望大家將這八個字銘記於心，以自強不息勉勵自己，保持不斷虛心學習的動機，跨出原先熟悉的知識領域和人生領域；以厚德載物勉勵自己，跨領域的目的是創造自己和人群更大的價值，積厚自我，承担未來所面對的事物。恭喜大家，並祝福大家擁有一個美麗的知識旅程和人生旅程！
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownVerbLIST = articut.getVerbStemLIST(unknownResultDICT)
    print("清大：")
    print(wordExtractor(unknownVerbLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個動詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballVerbLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballVerbLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownVerbLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[台大 vs. 清大] 的動詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[梅克爾 vs. 清大] 的動詞餘弦相似度:{}".format(basketball2unknownSIM))


    # 取得「名詞」做為特徵列表
    baseballNounLIST = articut.getNounStemLIST(baseballResultDICT)
    print("台大：")
    print(wordExtractor(baseballNounLIST, unify=False))
    print("\n")
    print("梅克爾：")
    basketballNounLIST = articut.getNounStemLIST(basketballResultDICT)
    print(wordExtractor(basketballNounLIST, unify=False))
    print("\n")



    # 未知類別的文本(成大)
    unknownSTR01 = """賴市長、演講貴賓李鴻源教授、今天蒞臨會場的貴賓們、本校各位師長、各位畢業生家長、今天最重要的主角，全體畢業同學們，大家晚安：
    創校84年的成功大學今天要為這個熱切期待進步的台灣、等待和平的世界，貢獻有高度專業知能、具樸質人文素養、同時懷抱著服務人群的最高情操的2591位學士、2986位碩士、360位博士，請各位畢業生、各位家長、各位師長、各界貴賓一起用熱烈的掌聲為我們互相賀喜！84年來成功大學因為這個城市的陽光照耀、雨水滋潤、文化培育、人情溫暖而成長、因為歷任師長職工的耕耘而茁壯、因為全球十四萬校友在各行各業的成就與奉獻而偉大！歡迎今天所有現場的畢業同學在此刻就要加入這個偉大的行列！連年以來，成功大學的畢業生已經成爲企業之最愛，因為我們合群、踏實、具團隊執行力：我希望所有的畢業同學要珍惜這些前期學長學姊用心血努力奠定的美好聲名！今年，我們在全國的調查評比中，無論是國際視野或創新創意的表現上首度名列第一，在在顯示，社會各界對成功大學畢業生有著更高、更遠的期待，作爲台灣舉足輕重的頂尖大學，我們更有義務在未來創造出社會上最尊敬的企業、以回饋世界！畫家保羅高更有一幅題為「我們從何處來？我們是誰？我們向何處去？」的名作，其中對於生命的意義有一連串的探索：回想自小到大我們所接受的教育無一不在努力使我們成為知識豐富的人，期待我們運用這些知識解決社會上面對生存發展的各種挑戰！而今年，畢聯會同學籌辦典禮的主題，也以「邁向未來」為主題，而我想與各位畢業同學共勉的是，在企圖心起飛的時刻，要用同理心深刻凝視弱勢的需求、理解差異的根源，用善念存心，去尋找我們的知識能力可以在宇宙人群間貢獻的角落與方式！當然，過去幾年大家在大學校園生活與學習中所被呵護的自由在各位離開校園、獨立行事時則需要各位有更成熟、深層的省思，當民主與法治能夠並存、互相尊重，才是進步的完整動力，也才能實質的帶動改變。近來我在校園走動時，常常望見「成功入口」的畢業形象設計，內心的感受十分複雜！幾年前各位進入成功大學之際，大約都懷抱著「從此成功」的夢想，如果此刻你已經有更多的信心去實現那個夢想，作為師長，當然無比安慰！但是，如果你以為畢業的此刻，必然是通向成功的勝利大道，身為師長，更希望你具備正面看待挫折的心智，那也正是生命中最重要的養分，讓我們能夠更加認識自己、增長智慧；失敗難免讓我們恐懼、不安，但是，只要心念高遠、在經營個人幸福的同時，看見大我的福祉，努力在歷史的長河中紮紮實實留下屬於自己與大社會共享的足跡，你和這一所大學的意義自然也會不同！而那也正是我和行政同仁接任校務工作短短數月以來，面對紛擾、但是也看到希望的一些心得！當然，「一日成大人、永世成大人」，各位在成功大學的學業可能暫告一段落，而人生的學習才正要陸續展開，每一天，希望你都要看見更高、更遠的自己，每一天希望你都在社會進步、人類幸福的建設中留下自己努力付出的心意；讓我們珍惜這個緣份、一起奮鬥、互相榮耀！最後，容許我代表本校全體教職員工，感謝各位家長對成功大學的信任，使我們我機會跟各位的子弟一起成長，感謝社會各界對成功大學的支持，讓我們有資源栽培一流的人才，更感謝各位畢業同學過去幾年在這個校園生活、使這個校園豐富，祝福你們畢業快樂，鵬程萬里，各位來賓身體健康、平安如意。謝謝大家。
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownNounLIST = articut.getNounStemLIST(unknownResultDICT)
    print("成大：")
    print(wordExtractor(unknownNounLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個名詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballNounLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballNounLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownNounLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[台大 vs. 成大] 的名詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[梅克爾 vs. 成大] 的名詞餘弦相似度:{}".format(basketball2unknownSIM))




    # 取得「TF-IDF」做為特徵列表
    baseballTFIDFLIST = articut.analyse.extract_tags(baseballResultDICT)
    print("台大 TF-IDF：")
    print(baseballTFIDFLIST)
    print("\n")
    print("梅克爾 TF-IDF：")
    basketballTFIDFLIST = articut.analyse.extract_tags(basketballResultDICT)
    print(basketballTFIDFLIST)
    print("\n")



    # 未知類別的文本 (中山)
    unknownSTR01 = """昨晚在音樂系聽完音樂會，在返家車上看到晚報刊載，教育部黃部長昨日參加某校畢業典禮，認為校長致詞沒有創意，和黃部長三十年前畢業時聽到的大致相同，所以我為避免重蹈覆轍，決定立即更換成此講題。在億萬年前，地球是一片沼澤，住著許多生物，包括恐龍和蟑螂。恐龍當時稱霸天下，其數量驚人，種類繁多。後來沼澤漸漸乾涸，恐龍因而絕跡，但是蟑螂有高度適應變局的能力，所以存活下來。面對未來快速變化的世界，我們必須問自己，能不能像蟑螂一樣聰明， 屬於適者生存的一群。人類適應變局的能力當然與蟑螂是不同的，許多學者曾經分析了人類適應變局應當具備的人格特質與能力，我把它簡單歸納成一句話，那就是「勇於嘗試，不斷創新」。「臥虎藏龍」的導演李安，回到母校紐約大學獲頒名譽博士學位致詞時說：「我在學校裡沒學到什麼知識，而且學到的又早就忘光了」，隨後他又說：「不過我在這裡學到『不怕嘗試，學無止境』」的道理」。各位畢業同學，不管你擁有什麼學位，或學到多少東西，我希望你至少要記住「勇於嘗試，不斷創新」這八字真言。樂透彩電視開獎的節目主持人聶雲先生，為惠普科技的廣告配音，只講了一句「不斷創新HP」六個字，就得到十萬元的酬勞。大家可能很羨慕他擁有如此昂貴的價碼，但各位可知他為了錄這六個字，從早上九點進錄音室，直到下午五點才出來。大家又可知他十七歲便開始配音，嘗試過無數的角色，經歷了多少次的失敗，才逐步做出口碑，獲得別人的肯定。根據報載，美國一位 103歲的老奶奶，擔任今年初在美國鹽湖城舉行的冬季奧運會傳遞聖火的火炬手 。這是奧運會史上最高齡的選手。加拿大多倫多有位15歲的少女，手肘和膝蓋以下的四肢都沒有了，可是卻以15小時的時間，游泳橫渡了20公里的美加邊界的艾瑞湖，成為第一位橫渡艾瑞湖的殘障者。各位同學！只要勇於嘗試，就一定能預約成功，生命就有新的出口。
    有位建築師 Yamazaki是美籍日本人，雖然從小在美國長大，英語流利程度與美國人無異，但從讀書到就業，由於是有色人種，始終遭到排擠，Yamazaki並不氣餒，自己開了一家建築師事務所，透過競圖爭取業務。由於他勇於嘗試，不斷創新，在設計沙烏地阿拉伯『達蘭機場大廈』時，設計出充滿天方夜譚情調的現代建築，贏得國王的讚賞，並把這棟建築物獨特的外型，做為沙烏地阿拉伯鈔票的圖案。從此Yamazaki聲名遠播，終於獲得紐約新澤西港務局的邀請，負責設計「紐約世貿中心大樓」，這兩棟外型完全一樣的超高大樓，曾被喻為「全世界設計最好的超高層建築」，現在雖然世貿大樓已成廢墟，Yamazaki也在十餘年前就去世了，但他不畏挫折勇於嘗試不斷創新的鬥志，告訴我們，只要我們願意，人人可以設計、建造出自己生命中的摩天大樓。各位同學，世界是不斷的被更新重建，過去工業社會，寄信到美國需要至少一週時間，現在是網路世界，我們發出電子郵件，美國的朋友在前一天就可收到。下一個生物科技的世界或奈米世界即將到來，我們尚無法預知未來可能發生的變動，但唯有秉持「勇於嘗試不斷創新」的精神，才能迎接新世界的來臨。
    美國南加州大學附近有個加油站，大家都稱加油站的加油老人是「Professor」，為什麼這樣稱呼呢？原來這位老人年輕時是「真空管理論」的權威教授，發表過很多論文，可是當「電晶體」的理論出現後，這位教授不願接受改變，不願學習新的理論，不願創新，就被大學淘汰了。為了打發老年無聊的時間，便跑到加油站賺外快。花蓮女中有位工友林天來先生，在圖書館擔任管理員，因而愛上看書，後因徵文比賽得獎而與天下文化出版公司結緣，便從花蓮到台北工作，從倉庫管理員做起。十三年來，林先生任過行銷、企劃、副理、經理、副總經理等許多職務，職務雖然不同，但林先生始終把握公餘時間充實知識，持續學習，在崗位上不斷創新，由於工作表現優異，今年二月被擢昇為總經理。一位高工畢業生，就能體認「勇於嘗試，不斷創新」的道理，十三年後終於成為著名出版公司總經理。
    各位同學！人生最怕失去信心與勇氣，也最怕放棄自己，觀念改變，行動改變，命 運就會改變。星雲大師連小學都沒有畢業，但他創辦人間佛教，全球都有分院，信徒無數，因此工作非常忙碌，平均一年要繞地球兩週半，可是不管如何忙碌，他始終手不釋卷，博覽群書，利用閒暇時間，竟然完成了二十餘部膾炙人口的著作。最近星雲大師在日本演講，講題是「發心與發展」，他說「發心就是要自我建設，發展就是要建設世界」。各位同學！今天你們帶著老師的叮嚀、家長的期許，踏入多變的社會，不論你在中山學到多少知識，但請不要忘記以「勇於嘗試」的心境來自我建設，以「不斷創新」的精神持續充實自己，來建設世界。各位同學，你到底會不會比蟑螂聰明，是你自己的選擇。聖經上說「專心尋求，就必尋見」。祝福大家！最後，敬祝大家鵬程萬里！
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownTFIDFLIST = articut.analyse.extract_tags(unknownResultDICT)
    print("中山 TF-IDF：")
    print(unknownTFIDFLIST)
    print("\n")


    # 利用 Counter() 模組計算每個 TF-IDF 特徵詞出現的次數
    baseballCOUNT = Counter(baseballTFIDFLIST)
    basketballCOUNT = Counter(basketballTFIDFLIST)
    unknownCOUNT = Counter(unknownTFIDFLIST)

    # 計算 [棒球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；計算 [籃球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[台大 vs. 中山] 的 TF-IDF 特徵詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[梅克爾 vs. 中山] 的 TF-IDF 特徵詞餘弦相似度:{}".format(basketball2unknownSIM))


    # 未知類別的文本 (台師大)
    unknownSTR01 = """今天是本校108學年度的畢業典禮，我非常高興地在這裡代表臺灣師大，向所有即將畢業的同學還有家長們祝賀。恭喜同學們學業有成，也祝福各位在踏出校園之後，迎接你們下一個階段的精采人生。
    今年春天以來，臺灣及世界各地面臨了新冠肺炎的威脅，在這場大規模的災難中，我們感受到了人類的無助與渺小。而臺灣師大比其他的學校，更切身體驗了病毒所帶來的衝擊與挑戰。但是我們堅定而勇敢地面對，不但完成了眾多僑外生的居家隔離工作；在同學確診後，相互照護，相互體諒，順利地實施了三週的全校遠距教學；全體師生更共同落實門禁管制，一起守護了校園的安全。在患難中，展現了師大人的真情與團結。
    在這次的疫情中，相信各位同學也有了前所未有的體悟：疫情限制了我們的活動，打亂了我們原先的安排，也改變了我們社交的模式；更多的居家時間，讓我們有更多的機會與家人相處，也增加了更多自我省思的時間。疫情讓我們反思人類與自然的關係，讓我們思考自我與社會的共生連結，更迫使我們重新評估全球化趨勢下的變局與轉機。 這些反思，也是各位未來生涯中必須關注的課題。
    面對瞬息萬變的世界，唯有隨時做好因應的準備，讓知識作為我們的導航，讓好奇心保持我們探索未知的熱情，讓不斷學習開闊我們的視野。更重要的是，當挑戰來臨時，我們要有求新求變的覺悟，以及採取行動的勇氣。然而，我們也相信在變動中，仍然有著不變的真理。我們必須持續地善待周遭的每一個人、關心社會、發揮自身良善的力量，讓世界有更多正向的互動。
    從今天起，大家就要正式加入臺灣師大優秀校友的行列了！因為有你，臺灣師大可以更加的茁壯！期盼各位同學以後繼續與母校維持緊密的關係，讓我們一起努力，持續進步。最後，祝福你們，展翅高飛！謝謝大家。
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownTFIDFLIST = articut.analyse.extract_tags(unknownResultDICT)
    print("台師大 TF-IDF：")
    print(unknownTFIDFLIST)
    print("\n")


    # 利用 Counter() 模組計算每個 TF-IDF 特徵詞出現的次數
    baseballCOUNT = Counter(baseballTFIDFLIST)
    basketballCOUNT = Counter(basketballTFIDFLIST)
    unknownCOUNT = Counter(unknownTFIDFLIST)

    # 計算 [棒球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；計算 [籃球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[台大 vs. 台師大] 的 TF-IDF 特徵詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[梅克爾 vs. 台師大] 的 TF-IDF 特徵詞餘弦相似度:{}".format(basketball2unknownSIM))



    # ############################################
    # ####
    # 未知類別的文本(耶魯1)
    unknownSTR01 = """2019 屆畢業生、學生家屬以及朋友們，上午好！很榮幸今天和你們一起在這。每年的畢業典禮既是起點，也是尾聲，既是滿懷著希望展望未來，也難免悲喜交加地依依惜別。對於我們所有人來說，這是一種錯綜複雜的情緒——而對於像我一樣的心理學家而言，這絕對是一個值得做田野調查的日子！好好享受所有這些感受吧！因為一生中很難再擁有這樣的體驗了。所以，此刻我要遵從一個很棒的耶魯傳統：請今天到在座的所有畢業生家屬和朋友們起立，並向 2019 屆的優秀畢業生們表示祝賀！現在有請 2019 屆全體畢業生們，感念所有支持你們走到今天的人，起立向他們致敬。謝謝！1974 年 9 月，當時耶魯大學的校長布魯斯特（Kingman Brewster Jr），與和你們坐在同樣位置的1978 屆學生們交談。他告訴他們：「在座的許多人剛剛經歷了道義上極其不滿的 10 年：反華萊士、反戰、反水門事件。我們很明確自己反對的是什麼，但我們幾乎忘記了知道自己要支持什麼以及如何去實現它有多困難。」這聽起來很熟悉嗎？今天，可能比以往任何時代都更容易知道自己反對什麼，也是比以往任何時代更難說出你支持的是什麼。每個人所反對的事物都不盡相同。也許你反對邊境築牆，而我反對槍支；你的鄰居反對貿易戰，你的堂兄反對墮胎。對於一些人來說，資本主義是問題；而另一些人則害怕社會主義的幽靈。但此刻，我打賭你們肯定都反對坐在沒有空調的老建築聽我長篇大論。所以，我打算要開門見山⋯⋯
    有多少人看過馬克思兄弟的電影？自從我刮鬍子後，雖然不再像以前那樣經常被誤認為是 Groucho Marx，但我依然對他的幽默情有獨鍾。Groucho 最精彩的表演之一，就是當他扮演大學校長。在電影 “Horse Feathers” 的開場中，這位赫胥黎學院的新校長被告知，校董們對他有「一些建議」，他突然唱起了這首歌：「我不知道他們有什麼要說的 無論如何都沒有區別 不管是什麼，我都將反對 無論是什麼，無論是誰說的 我會通通反對 你們的提議可能不錯 但讓我們要明白一件事：不管是什麼，我反對它。」我推薦你們去 YouTube 上看看這一段，不是現在就看。它仍然是一令人棒腹大笑作品。它好笑，是因為它很荒謬，也因為它有一點道理。這個道理不僅體現在大學校長身上，也適用於我們每個人身上。
    有多少次，我們在聽到某種觀點前就決定反對它？在我們還搞不清某件事是什麼之前就反對它，這樣的錯誤我們是否犯過？很多時候，我們反對什麼是取決於誰說出來的。如果那個觀點來自某個公眾人物、政客、媒體機構，我們就已經知道自己的立場。其中，部分原因是因為我們的公共話語已經變得如此可測，我們已經喪失了被震撼和被啟示的能力。談到可預測的，這一刻我想代表老一代，向千禧一代的你們提一下社交媒體的「罪與惡」。請聽我把話說完⋯
    社交媒體改變了我們的生活和人際關係。當然，它有很多優點，它使我們能夠快速地和世界各地的人分享新聞和信息。但它也增強了我們的憤怒感，加快了爭吵的擴散、剝奪了我們深思的時間和空間。社交媒體的信息接連不斷，你必須在某個熱門話題過氣前發表言論，於是我們用幾秒鐘就打出了自己支持（或反對）的立場。用 280 個字的推文來反對一件事是容易的，相反，要快速清楚地表達你支持什麼，則要困難得多。請大家不要誤會：憤怒的理由當然有很多。無論是我們這一代人，還是你們這一代，我們不僅面臨著嚴峻的道德挑戰，還面臨著存亡威脅：比如說，全球海平面上升，美國不平等加劇；世界各地的暴力衝突；社會組織渙散。正如葉慈的詩句「獵鷹再聽不見馴鷹人的呼聲」，我們想知道（體制的）中心是否還能支撐得住。
    指出錯誤只是開始，並不是結束。我理解消極性的衝動。像你們許多人一樣，我有時也會因為我們所面臨的挑戰和需要譴責的不公義現象而感到不知所措。然而，正是因為我們的挑戰如此艱鉅，只有憤怒是遠遠不夠的。指出錯誤只是我們工作的開始，而不是結束。捷克作家克利馬（Ivan Klíma ）寫道：「摧毀比創造更容易。這就是為什麼很多人公然表示他們拒絕的東西。但是如果有人問他們想要什麼，他們又會怎麼回答呢？」你會怎麼回答？我會怎麼回答？你追求的是什麼？
    克利馬的人生故事既有批判又有創造。他在 1931 年出生於布拉格，小時候被派往納粹集中營。他倖存下來，成為捷克斯洛伐克一位直言不諱的民主倡導者。但在 1968 年，隨著蘇聯的入侵和鎮壓，克利馬的言論被當局視為危險思想。他本可以逃走的，但他選擇了回到家鄉繼續他的工作，對抗共產主義政權。他成立地下作家組織，秘密傳閱彼此的手稿。18年來，他們創作了 300 部不同的藝術作品。他們是批評家，批評專政、暴力；但他們同時也是戲劇、小說和詩歌的創作者。他們想像並幫助創造了一個更美好的新世界。在座各位有任何願景嗎？一個更好的企業，一個更明智的學校，還是一個更強大的社區？無論你反對什麼，現在是時候創造你想要的東西了。
    在耶魯大學，你們學會了想像和創造。你們研究和探索了新的想法、創作藝術和音樂、進行體育運動競技、創立公司；近則服務鄰里，遠則奉獻世界。你們創造了一個充滿活力、多元和精彩的社區。請把這些經歷──裝入行囊，當你們需要鼓勵的時候，可以從中汲取力量。記住那個讓你驚喜的課堂、那段啟發你的對話、那位信任你的教授。要小心注意避免像作家莫瑞森（Toni Morrison）所說的「二流目標和二手思想」：「我們的過去是黯淡，我們的未來也是陰暗朦朧。」莫瑞森寫道，「但如果我們把這個世界看作是一場漫長而殘酷的遊戲，那我們就遇到了另一個謎，一個關於美、關於光、關於在頭顱上歌唱的金絲雀的謎。」追求某件事就像是探尋那些謎、那些光，是一種信念──堅信一個更完美的世界觸手可及，堅信我們能夠努力建成它。
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownNounLIST = articut.getNounStemLIST(unknownResultDICT)
    print("耶魯1：")
    print(wordExtractor(unknownNounLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個名詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballNounLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballNounLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownNounLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[台大 vs. 耶魯1] 的名詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[梅克爾 vs. 耶魯1] 的名詞餘弦相似度:{}".format(basketball2unknownSIM))


    # 取得「TF-IDF」做為特徵列表
    baseballTFIDFLIST = articut.analyse.extract_tags(baseballResultDICT)
    print("台大 TF-IDF：")
    print(baseballTFIDFLIST)
    print("\n")
    print("梅克爾 TF-IDF：")
    basketballTFIDFLIST = articut.analyse.extract_tags(basketballResultDICT)
    print(basketballTFIDFLIST)
    print("\n")



    # 未知類別的文本 (耶魯2)
    unknownSTR02 = """你追求的是甚麼？你可能會把這個問題丟回給我：校長，那你追求的又是什麼呢？我追求博雅教育的重塑力量──要求廣泛思考，質疑一切，並擁抱學習的樂趣。我追求真正意義上的「美國夢」──機會廣泛共享，接受教育是多數人的權利，而不是少數人的專利。我追求活躍且自由的思想交流，因為一所偉大學府的核心使命和我們的民主政體的良性運轉都需要它。我追求一個歡迎移民、窮人和被遺忘的人們的世界，而不是把他們拒之門外，或讓他們閉嘴。在那個世界，表現出同情和理解才是被視為成功和美好人生的真正標誌。
    這就是我所追求的。耶魯大學的使命中包含這句話：我們「致力於改善世界，為今天也為後人」，這個承諾並不會在畢業時便終止。你們很快便會離開耶魯，正如曾在耶魯大學學習和任教的文學家華倫（Robert Penn Warren ）寫道：「進入世界的動盪，走出歷史，又走進歷史。」的確，你們將進入歷史並創造歷史。今天環顧四周，我想起了之前的幾屆耶魯大學畢業生。那些有所追求的人。許多名字我們都知道，雖然也有其他一些人不那麼熟悉──總統和世界領袖，藝術家和企業高管，學者和科學家。
    像他們一樣，我知道各位將聽從召喚成為領導者和服務者，並在人類努力的每一個領域留下你們的印記。這就是耶魯的使命──這就是耶魯所追求的。作為耶魯的成員，我們相信什麼？我們相信，事實和專業，再加上創造力和智慧，可以改變世界。我們相信，教育和研究可以拯救生命，並使生活更有意義。我們相信，思想和行為的多樣性對人類進步至關重要。最重要的是，我們相信人類的聰明才智具有無限潛力；只要齊心協力，我們可以解決巨大的挑戰，並將光明和真理帶給一個極需要它的世界。在星期一的學位授予典禮上，我會授予你們耶魯學位的承載的「權利和責任」。你們的責任很重大，你們必須清楚你們的追求。
    你追求的是什麼？愛蓮娜·羅斯福（Eleanor Roosevelt，羅斯福總統夫人）曾說過：「從歷史的角度來看，明智者總是懷抱希望而非心存恐懼，勇於嘗試而非望而卻步。」作為一位學者和一個人，耶魯已經讓你準備好去嘗試，拿出勇氣和決心面對挑戰。我相信，你們離開耶魯時會帶著你們對彼此、對這個星球、對我們共同未來的責任感。運用你已經獲得的才能為他人和我們的社區服務，你們將會過上有意義、有目標的生活。沒有時間浪費，也沒有言語可浪費。正如年輕的巴布．狄倫（Bob Dylan）在 1965 年所唱的那樣：「不是忙著活著的人，就是忙著死去。」我們必須賦予生命新的思想，想象生存於這個世界的新方式，尋找惱人問題的新答案。現在是時候了。2019 屆學生們，請起立：我心懷喜悅向你們所取得的成就致敬，也為你們感到驕傲。請記得感謝所有幫你們走到今天的人們。請帶著感恩的心離開這裡，用你們的思想，聲音和雙手去想像，去創造你們希望看到的新世界，以此來回報你們在這裡所得到的饋贈。請問你們所追求的是什麼？祝賀你們，2019 屆的畢業生們！
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR02, userDefinedDictFILE="./mixedDICT.json")
    unknownVerbLIST = articut.getVerbStemLIST(unknownResultDICT)
    print("耶魯2：")
    print(wordExtractor(unknownVerbLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個動詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballVerbLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballVerbLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownVerbLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[台大 vs. 耶魯2] 的動詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[梅克爾 vs. 耶魯2] 的動詞餘弦相似度:{}".format(basketball2unknownSIM))





    # 取得「名詞」做為特徵列表
    baseballNounLIST = articut.getNounStemLIST(baseballResultDICT)
    print("台大名詞：")
    print(wordExtractor(baseballNounLIST, unify=False))
    print("\n")
    print("梅克爾名詞：")
    basketballNounLIST = articut.getNounStemLIST(basketballResultDICT)
    print(wordExtractor(basketballNounLIST, unify=False))
    print("\n")

    # 未知類別的文本 (耶魯3)
    unknownSTR02 = """很多時候，我們反對什麼是取決於誰說出來的。如果那個觀點來自某個公眾人物、政客、媒體機構，我們就已經知道自己的立場。其中，部分原因是因為我們的公共話語已經變得如此可測，我們已經喪失了被震撼和被啟示的能力。談到可預測的，這一刻我想代表老一代，向千禧一代的你們提一下社交媒體的「罪與惡」。請聽我把話說完⋯⋯
    社交媒體改變了我們的生活和人際關係。當然，它有很多優點，它使我們能夠快速地和世界各地的人分享新聞和信息。但它也增強了我們的憤怒感，加快了爭吵的擴散、剝奪了我們深思的時間和空間。社交媒體的信息接連不斷，你必須在某個熱門話題過氣前發表言論，於是我們用幾秒鐘就打出了自己支持（或反對）的立場。用 280 個字的推文來反對一件事是容易的，相反，要快速清楚地表達你支持什麼，則要困難得多。請大家不要誤會：憤怒的理由當然有很多。無論是我們這一代人，還是你們這一代，我們不僅面臨著嚴峻的道德挑戰，還面臨著存亡威脅：比如說，全球海平面上升，美國不平等加劇；世界各地的暴力衝突；社會組織渙散。正如葉慈的詩句「獵鷹再聽不見馴鷹人的呼聲」，我們想知道（體制的）中心是否還能支撐得住。
    指出錯誤只是開始，並不是結束。我理解消極性的衝動。像你們許多人一樣，我有時也會因為我們所面臨的挑戰和需要譴責的不公義現象而感到不知所措。然而，正是因為我們的挑戰如此艱鉅，只有憤怒是遠遠不夠的。指出錯誤只是我們工作的開始，而不是結束。捷克作家克利馬（Ivan Klíma ）寫道：「摧毀比創造更容易。這就是為什麼很多人公然表示他們拒絕的東西。但是如果有人問他們想要什麼，他們又會怎麼回答呢？」你會怎麼回答？我會怎麼回答？你追求的是什麼？
    克利馬的人生故事既有批判又有創造。他在 1931 年出生於布拉格，小時候被派往納粹集中營。他倖存下來，成為捷克斯洛伐克一位直言不諱的民主倡導者。但在 1968 年，隨著蘇聯的入侵和鎮壓，克利馬的言論被當局視為危險思想。他本可以逃走的，但他選擇了回到家鄉繼續他的工作，對抗共產主義政權。他成立地下作家組織，秘密傳閱彼此的手稿。18年來，他們創作了 300 部不同的藝術作品。他們是批評家，批評專政、暴力；但他們同時也是戲劇、小說和詩歌的創作者。他們想像並幫助創造了一個更美好的新世界。在座各位有任何願景嗎？一個更好的企業，一個更明智的學校，還是一個更強大的社區？無論你反對什麼，現在是時候創造你想要的東西了。
    在耶魯大學，你們學會了想像和創造。你們研究和探索了新的想法、創作藝術和音樂、進行體育運動競技、創立公司；近則服務鄰里，遠則奉獻世界。你們創造了一個充滿活力、多元和精彩的社區。請把這些經歷──裝入行囊，當你們需要鼓勵的時候，可以從中汲取力量。記住那個讓你驚喜的課堂、那段啟發你的對話、那位信任你的教授。要小心注意避免像作家莫瑞森（Toni Morrison）所說的「二流目標和二手思想」：「我們的過去是黯淡，我們的未來也是陰暗朦朧。」莫瑞森寫道，「但如果我們把這個世界看作是一場漫長而殘酷的遊戲，那我們就遇到了另一個謎，一個關於美、關於光、關於在頭顱上歌唱的金絲雀的謎。」追求某件事就像是探尋那些謎、那些光，是一種信念──堅信一個更完美的世界觸手可及，堅信我們能夠努力建成它。 """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR02, userDefinedDictFILE="./mixedDICT.json")
    unknownTFIDFLIST = articut.analyse.extract_tags(unknownResultDICT)
    print("耶魯3 TF-IDF：")
    print(unknownTFIDFLIST)
    print("\n")


    # 利用 Counter() 模組計算每個 TF-IDF 特徵詞出現的次數
    baseballCOUNT = Counter(baseballTFIDFLIST)
    basketballCOUNT = Counter(basketballTFIDFLIST)
    unknownCOUNT = Counter(unknownTFIDFLIST)

    # 計算 [棒球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；計算 [籃球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[台大 vs. 耶魯3] 的 TF-IDF 特徵詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[梅克爾 vs. 耶魯3] 的 TF-IDF 特徵詞餘弦相似度:{}".format(basketball2unknownSIM))

   
   
    # 未知類別的文本 (歐普拉)
    unknownSTR02 = """歐普拉首先在開頭表示，今年因為疫情影響，畢業典禮都紛紛取消，畢業生無法像過去一樣上台領獎、接受親人獻花，不過他們將獲得臉書上所有參加這場線上典禮的人的祝福，她在此也要向他們致意，2020年的畢業典禮，其實比以往的畢業典禮多了更多希望、願景與對畢業生的期待。

    歐普拉接著談起「畢業」的意義，拉丁文的原意是「跨過某個東西的一步」，在過去煉金術士也把這個詞作為新元素煉成的意思，她坦言，無法告訴畢業生將要面對怎樣的未來，但面對不可知的未來，他們需要保有的是相同的勇氣、決心、膽識與想像力，這些將讓他們克服未來人生中所會遇到的困難。綻放自我、推己及人「新冠疫情也只是一種不確定因素罷了，你們要學會與未知的挑戰和共處。」歐普拉鼓勵畢業生說，新冠疫情只是人生中的一個小插曲，但是疫情將許多既有的、結構性的社會問題放得更大，以不平等為例，不平等讓窮人無法獲得健保、移民因為受歧視而躲藏、囚犯無法保持社交距離，以及黑人與女人不敢在街上慢跑。

    她以金恩博士的話「我們是命運共同體、無法逃脫的互助網。而直接影響自身的，也會間接影響他人。」呼籲2020年的畢業生，人類的所作所為都會互相影響，因此面對疫情挑戰，要維持健康的身心靈，並接受家人最溫暖的關懷，「讓自己好、讓大家更好。」「你的社會服務價值是什麼？」根據《每日郵報》報導，歐普拉強調，無論是老師、醫護人員、卡車司機、銀行櫃員，即使在染疫的高風險下，他們仍然發揮自己的社會價值、盡忠職守，因此她要畢業生找到自己的社會價值，你將以什麼樣的專長、熱情來服務你的社區、甚至是全世界？

    她最後期許畢業生發揮所長、創造力，並勇於發聲，為遭受疫情重挫的世界創造更多平等、公義與歡笑。""".replace(" ", "").replace("\n", "")
    
    unknownResultDICT = articut.parse(unknownSTR02, userDefinedDictFILE="./mixedDICT.json")
    unknownNounLIST = articut.getNounStemLIST(unknownResultDICT)
    print("歐普拉：")
    print(wordExtractor(unknownNounLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個動詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballNounLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballNounLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownNounLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[台大 vs. 歐普拉] 的名詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[梅克爾 vs. 歐普拉] 的名詞餘弦相似度:{}".format(basketball2unknownSIM))




    # 取得「TF-IDF 特徵詞」做為特徵列表
    baseballTFIDFLIST = articut.analyse.extract_tags(baseballResultDICT)
    print("台大 TF-IDF：")
    print(baseballTFIDFLIST)
    print("\n")
    print("梅克爾 TF-IDF：")
    basketballTFIDFLIST = articut.analyse.extract_tags(basketballResultDICT)
    print(basketballTFIDFLIST)
    print("\n")



  