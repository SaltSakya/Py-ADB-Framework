import os
import time
import random

from threading import Thread

import numpy as np
from json import loads, dumps
from requests import get, post
from requests.cookies import RequestsCookieJar, cookiejar_from_dict

from PIL import Image
import qrcode
import qrcode_terminal

from js_tools import Number

# 此脚本会从吗哩吗哩工具箱爬取数据
# https://game.bilibili.com/tool/pd/

DATA_PATH = os.path.join("..", "Resources", "data")
HERO_CARDS_PATH = os.path.join("..", "Resources", "data", "hero_cards")
HERO_ICON_PATH = os.path.join("..", "Resources", "data", "hero_icons")
SUPPORT_CARDS_PATH = os.path.join("..", "Resources", "data", "support_cards")
SCRIPT_PATH = os.path.join("..", "Resources", "data", "script")

for path in [DATA_PATH, HERO_CARDS_PATH, HERO_ICON_PATH, SUPPORT_CARDS_PATH, SCRIPT_PATH]:
    if not os.path.exists(path):
        os.makedirs(path)

class Rarity:
    Unlimit = 1
    At_Least_2_Star = 2
    At_Least_3_Star = 3
    At_Least_4_Star = 4
    At_Least_5_Star = 5
    At_Least_6_Star = 6
    At_Least_7_Star = 7
    At_Least_8_Star = 8
    At_Least_9_Star = 9
    Self_At_Least_1_Star = 1
    Self_At_Least_2_Star = 2
    Self_At_Least_3_Star = 3

class MScrawler:

    Cookies = None

    PRINT_QRCODE_IN_TERMINAL = False

    @staticmethod
    def Init():
        MScrawler.Cookies = MScrawler.LoadCookies()

    @staticmethod
    def LoginBiliBili() -> RequestsCookieJar:
        # 定义 url
        login_url = "https://passport.bilibili.com/x/passport-login/web/qrcode/generate?"
        poll_url = "https://passport.bilibili.com/x/passport-login/web/qrcode/poll?"

        # 加载二维码
        r = get(login_url)
        data = r.json()

        # 读取二维码的 url 和 key
        qrcode_url = data["data"]["url"]
        qrcode_key = data["data"]["qrcode_key"]

        # 显示二维码
        if MScrawler.PRINT_QRCODE_IN_TERMINAL:
            # 在命令行绘制二维码
            qrcode_terminal.draw(qrcode_url)
        else:
            # 打开图片二维码文件
            Thread(target=qrcode.make(qrcode_url).show).start()

        # Query 参数
        params = {
            "qrcode_key": qrcode_key,
            "source": "main_web"
        }

        # 轮询
        while True:
            time.sleep(2)
            r = get(poll_url, params=params)
            if r.json()["data"]["code"] == 0:
                break
        
        # 返回 cookie，类型为 RequestsCookieJar
        return r.cookies

    @staticmethod
    def LoadCookies(forceLogin = False) -> RequestsCookieJar:
        # 参数配置强行重新登录读取或 Cookies 文件不存在
        if forceLogin or not os.path.exists("cookies.dat"):
            cookies = MScrawler.LoginBiliBili()
            MScrawler.SaveCookies(cookies)
        # 直接读取 Cookies 文件
        else:
            with open("cookies.dat", "r", encoding="utf-8") as f:
                cookies = cookiejar_from_dict(loads(f.read()))
        # 返回 Cookies
        return cookies

    @staticmethod
    def SaveCookies(cookies: RequestsCookieJar):
        # 写入 Cookies
        with open("cookies.dat", "w", encoding="utf-8") as f:
            f.write(dumps(cookies.get_dict()))

    @staticmethod
    def Factors():
        url = "https://api.game.bilibili.com/game/player/tools/uma/factors?"
        params = {
            "ts": str(int(time.time()*1000)),
            "nonce": Auth.RandomUUID(),
            "appkey": "d053991039404237a44023da011d3e08"
        }
        params["sign"] = Auth.Get(params)
        r = get(url, cookies=MScrawler.Cookies, params=params)
        return r.json()

    @staticmethod
    def HeroCards():
        url = "https://api.game.bilibili.com/game/player/tools/uma/hero_cards?"
        params = {
            "ts": str(int(time.time()*1000)),
            "nonce": Auth.RandomUUID(),
            "appkey": "d053991039404237a44023da011d3e08"
        }
        params["sign"] = Auth.Get(params)
        r = get(url, cookies=MScrawler.Cookies, params=params)
        return r.json()
    
    @staticmethod
    def SupportCards():
        url = "https://api.game.bilibili.com/game/player/tools/uma/support_cards?"
        params = {
            "ts": str(int(time.time()*1000)),
            "nonce": Auth.RandomUUID(),
            "appkey": "d053991039404237a44023da011d3e08"
        }
        params["sign"] = Auth.Get(params)
        r = get(url, cookies=MScrawler.Cookies, params=params)
        return r.json()

    @staticmethod
    def ScriptList():
        url = "https://api.game.bilibili.com/game/player/tools/uma/script_list?"
        params = {
            "ts": str(int(time.time()*1000)),
            "nonce": Auth.RandomUUID(),
            "appkey": "d053991039404237a44023da011d3e08"
        }
        params["sign"] = Auth.Get(params)
        r = get(url, cookies=MScrawler.Cookies, params=params)
        return r.json()
    
    @staticmethod
    def HeroCardDetail(hero_card_id: int):
        url = "https://api.game.bilibili.com/game/player/tools/uma/hero_card_detail?"
        params = {
            "hero_card_id": str(hero_card_id),
            "ts": str(int(time.time()*1000)),
            "nonce": Auth.RandomUUID(),
            "appkey": "d053991039404237a44023da011d3e08",
        }
        params["sign"] = Auth.Get(params)
        r = get(url, cookies=MScrawler.Cookies, params=params)
        return r.json()
    
    @staticmethod
    def SupportCardDetail(support_card_ids: int):
        url = "https://api.game.bilibili.com/game/player/tools/uma/support_card_detail?"
        params = {
            "support_card_ids": str(support_card_ids),
            "ts": str(int(time.time()*1000)),
            "nonce": Auth.RandomUUID(),
            "appkey": "d053991039404237a44023da011d3e08"
        }
        params["sign"] = Auth.Get(params)
        r = get(url, cookies=MScrawler.Cookies, params=params)
        return r.json()
    
    @staticmethod
    def ScriptDetail(script_id: int):
        url = "https://api.game.bilibili.com/game/player/tools/uma/script_detail?"
        params = {
            "script_id": str(script_id),
            "ts": str(int(time.time()*1000)),
            "nonce": Auth.RandomUUID(),
            "appkey": "d053991039404237a44023da011d3e08"
        }
        params["sign"] = Auth.Get(params)
        r = get(url, cookies=MScrawler.Cookies, params=params)
        return r.json()

    @staticmethod
    def MakeMethod(
        card_ids:list|int=None,
        blue_factor:int=None,
        blue_rarity:int=Rarity.Unlimit,
        blue_self_rarity:int=None,
        red_factor:int=None,
        red_rarity:int=Rarity.Unlimit,
        red_self_rarity:int=None,
        green_factor:int=None,
        green_rarity:int=Rarity.Unlimit,
        green_self_rarity:int=None,
        story_factor:int=None,
        story_rarity:int=Rarity.Unlimit,
        story_self_rarity:int=None,
        skill_factor:int=None,
        skill_rarity:int=Rarity.Unlimit,
        skill_self_rarity:int=None,
        race_factor:int=None,
        race_rarity:int=Rarity.Unlimit,
        race_self_rarity:int=None,
        min_win_race_count:int=0
    ) -> dict:
        data = {
            #"card_ids": "100101,100301",
            "filter_follow_reach_limit": 1,
            #"min_win_race_count": "6",
            #"factor_filters": "[{\"type\":1,\"values\":[{\"num\":1,\"rarity\":1}]},{\"type\":2,\"values\":[{\"num\":22,\"rarity\":2}]},{\"type\":3,\"values\":[{\"num\":100901,\"rarity\":4}]},{\"type\":4,\"values\":[{\"num\":20021,\"self_rarity\":1}]},{\"type\":5,\"values\":[{\"num\":10022,\"self_rarity\":3}]},{\"type\":6,\"values\":[{\"num\":30002,\"rarity\":8}]}]",
            "page_size": 20,
            "page_num": 1,
            "ts": int(time.time()*1000),
            "nonce": Auth.RandomUUID(),
            "appkey": "d053991039404237a44023da011d3e08"
        }
        if card_ids:
            if type(card_ids) == int:
                data["card_ids"] = str(card_ids)
            if type(card_ids) == list:
                data["card_ids"] = ",".join([str(i) for i in card_ids])
        factor_filters = list()
        if blue_factor:
            factor_filters.append({
                "type": 1,
                "values": [{
                    "num": blue_factor,
                    "self_rarity" if blue_self_rarity else "rarity": blue_self_rarity if blue_self_rarity else blue_rarity
                }]
            })
        if red_factor:
            factor_filters.append({
                "type": 2,
                "values": [{
                    "num": red_factor,
                    "self_rarity" if red_self_rarity else "rarity": red_self_rarity if red_self_rarity else red_rarity
                }]
            })
        if green_factor:
            factor_filters.append({
                "type": 3,
                "values": [{
                    "num": green_factor,
                    "self_rarity" if green_self_rarity else "rarity": green_self_rarity if green_self_rarity else green_rarity
                }]
            })
        if skill_factor:
            factor_filters.append({
                "type": 4,
                "values": [{
                    "num": skill_factor,
                    "self_rarity" if skill_self_rarity else "rarity": skill_self_rarity if skill_self_rarity else skill_rarity
                }]
            })
        if race_factor:
            factor_filters.append({
                "type": 5,
                "values": [{
                    "num": race_factor,
                    "self_rarity" if race_self_rarity else "rarity": race_self_rarity if race_self_rarity else race_rarity
                }]
            })
        if story_factor:
            factor_filters.append({
                "type": 6,
                "values": [{
                    "num": story_factor,
                    "self_rarity" if story_self_rarity else "rarity": story_self_rarity if story_self_rarity else story_rarity
                }]
            })
        if len(factor_filters) > 0:
            data["factor_filters"] = str(dumps(factor_filters)).replace(" ", "")
        if min_win_race_count:
            data["min_win_race_count"] = str(min_win_race_count)
        data["sign"] = Auth.Get(data)
        return data

    @staticmethod
    def SearchHeroCard(data:dict):
        raise NotImplementedError("该功能目前不可用")
        # 目前不可用
        url = "https://api.game.bilibili.com/game/player/tools/uma/hero_card/search"
        r = post(url, cookies=MScrawler.Cookies, data=data)
        return r.json()
    
    @staticmethod
    def SearchSupportCard(card_ids:list|int):
        raise NotImplementedError("该功能目前不可用")
        # 目前不可用
        url = "https://api.game.bilibili.com/game/player/tools/uma/support_card/search"
        data = {
            "filter_follow_reach_limit": 1,
            "page_size": 20,
            "page_num": 1,
            "ts": int(time.time()*1000),
            "nonce": "8b1ed169-5935-4f18-be7f-690fbb9b11d8",
            "appkey": "d053991039404237a44023da011d3e08",
            "sign": "ec629350abfa12cffe40c6dd76b2805c"
        }
        r = post(url, cookies=MScrawler.Cookies, params=data)
        return r

class Auth:

    @staticmethod
    def RandomUUID():
        def randstr(length):
            "".join([random.choice("0123456789abcdef") for _ in range(length)])
        return f"{randstr(8)}-{randstr(4)}-{randstr(4)}-{randstr(4)}-{randstr(12)}"

    @staticmethod
    def MakeStringData(data):
        keys = list(data.keys())
        keys.sort()
        return "&".join([f"{k}={data[k]}" for k in keys]) + '&secret=Hs8yIaC/AtYoBEO6jsQuNfDM9nK6ecFaXi2CttwwKxQ='
        #i = "appkey={}&nonce={}&support_card_ids={}&ts={}&secret=Hs8yIaC/AtYoBEO6jsQuNfDM9nK6ecFaXi2CttwwKxQ="
        #'&secret=Hs8yIaC/AtYoBEO6jsQuNfDM9nK6ecFaXi2CttwwKxQ='

    @staticmethod
    def bytesToWords(r):
        o = 0
        i = 0
        n = list()

        for o in range(len(r)):
            while len(n) <= (i >> 5):
                n.append(0)
            n[i>>5] |= r[o] << 24 - i % 32
            i += 8
        return n

    @staticmethod
    def wordsToBytes(r):
        n = list()
        for o in range(0, len(r)*32, 8):
            n.append(r[o >> 5] >> 24 - o % 32 & 255)
        return n
    
    @staticmethod
    def off(i, a, s, l, u, f, h):
        g = i + (a & s | ~a & l) + (u >> 0) + h
        return ((g<<f) | g >> 32 - f) + a
    
    @staticmethod
    def ogg(i, a, s, l, u, f, h):
        g = i + (a & l | s & ~l) + (u >> 0) + h
        return ((g<<f) | g >> 32 - f) + a
    
    @staticmethod
    def ohh(i, a, s, l, u, f, h):
        g = i + (a ^ s ^ l) + (u >> 0) + h
        return ((g<<f) | g >> 32 - f) + a
    
    @staticmethod
    def oii(i, a, s, l, u, f, h):
        g = i + (s ^ (a | ~l)) + (u >> 0) + h
        return ((g<<f) | g >> 32 - f) + a
    
    @staticmethod
    def rotl(r, n):
        return r << n | r >> 32 - n

    @staticmethod
    def endian(r):
        if type(r) != list:
            return Auth.rotl(r, 8) & 16711935 | Auth.rotl(r, 24) & 4278255360
        for n in range(len(r)):
            r[n] = Auth.endian(r[n])
        return r
    
    @staticmethod
    def bytesToHex(r):
        n = list()
        for o in range(len(r)):
            n.append(np.base_repr((r[o] >> 4).n, base=16))
            n.append(np.base_repr((r[o] & 15).n, base=16))
        return "".join(n)

    @staticmethod
    def o(i):
        i = [ord(char) for char in i]
        s = Auth.bytesToWords(i)
        l = len(i) * 8
        u = Number(1732584193)
        f = Number(-271733879)
        h = Number(-1732584194)
        g = Number(271733878)
        for C in range(len(s)):
            # 注意此处为无符号右移
            s[C] = Number((s[C] << 8 | s[C] >> 24) & 16711935 | (s[C] << 24 | s[C] >> 8) & 4278255360)

        s[l >> 5] |= Number(128) << l % 32
        while len(s) <= (l + 64 >> 9 << 4) + 14:
            s.append(Number(0))
        s[(l + 64 >> 9 << 4) + 14] = Number(l)

        while len(s)%16:
            s.append(Number(0))


        for C in range(0, len(s), 16):
            b = Auth.off
            I = Auth.ogg
            k = Auth.ohh
            R = Auth.oii

            F = u
            dollar = f
            P = h
            _ = g

            u = b(u, f, h, g, s[C + 0], 7, -680876936)        
            g = b(g, u, f, h, s[C + 1], 12, -389564586)        
            h = b(h, g, u, f, s[C + 2], 17, 606105819)        
            f = b(f, h, g, u, s[C + 3], 22, -1044525330)        
            u = b(u, f, h, g, s[C + 4], 7, -176418897)        
            g = b(g, u, f, h, s[C + 5], 12, 1200080426)        
            h = b(h, g, u, f, s[C + 6], 17, -1473231341)        
            f = b(f, h, g, u, s[C + 7], 22, -45705983)        
            u = b(u, f, h, g, s[C + 8], 7, 1770035416)        
            g = b(g, u, f, h, s[C + 9], 12, -1958414417)        
            h = b(h, g, u, f, s[C + 10], 17, -42063)        
            f = b(f, h, g, u, s[C + 11], 22, -1990404162)        
            u = b(u, f, h, g, s[C + 12], 7, 1804603682)        
            g = b(g, u, f, h, s[C + 13], 12, -40341101)        
            h = b(h, g, u, f, s[C + 14], 17, -1502002290)        
            f = b(f, h, g, u, s[C + 15], 22, 1236535329)        
            u = I(u, f, h, g, s[C + 1], 5, -165796510)        
            g = I(g, u, f, h, s[C + 6], 9, -1069501632)        
            h = I(h, g, u, f, s[C + 11], 14, 643717713)        
            f = I(f, h, g, u, s[C + 0], 20, -373897302)        
            u = I(u, f, h, g, s[C + 5], 5, -701558691)        
            g = I(g, u, f, h, s[C + 10], 9, 38016083)        
            h = I(h, g, u, f, s[C + 15], 14, -660478335)        
            f = I(f, h, g, u, s[C + 4], 20, -405537848)        
            u = I(u, f, h, g, s[C + 9], 5, 568446438)        
            g = I(g, u, f, h, s[C + 14], 9, -1019803690)        
            h = I(h, g, u, f, s[C + 3], 14, -187363961)        
            f = I(f, h, g, u, s[C + 8], 20, 1163531501)        
            u = I(u, f, h, g, s[C + 13], 5, -1444681467)        
            g = I(g, u, f, h, s[C + 2], 9, -51403784)        
            h = I(h, g, u, f, s[C + 7], 14, 1735328473)        
            f = I(f, h, g, u, s[C + 12], 20, -1926607734)        
            u = k(u, f, h, g, s[C + 5], 4, -378558)        
            g = k(g, u, f, h, s[C + 8], 11, -2022574463)        
            h = k(h, g, u, f, s[C + 11], 16, 1839030562)        
            f = k(f, h, g, u, s[C + 14], 23, -35309556)        
            u = k(u, f, h, g, s[C + 1], 4, -1530992060)        
            g = k(g, u, f, h, s[C + 4], 11, 1272893353)        
            h = k(h, g, u, f, s[C + 7], 16, -155497632)        
            f = k(f, h, g, u, s[C + 10], 23, -1094730640)        
            u = k(u, f, h, g, s[C + 13], 4, 681279174)        
            g = k(g, u, f, h, s[C + 0], 11, -358537222)        
            h = k(h, g, u, f, s[C + 3], 16, -722521979)        
            f = k(f, h, g, u, s[C + 6], 23, 76029189)        
            u = k(u, f, h, g, s[C + 9], 4, -640364487)        
            g = k(g, u, f, h, s[C + 12], 11, -421815835)        
            h = k(h, g, u, f, s[C + 15], 16, 530742520)        
            f = k(f, h, g, u, s[C + 2], 23, -995338651)        
            u = R(u, f, h, g, s[C + 0], 6, -198630844)        
            g = R(g, u, f, h, s[C + 7], 10, 1126891415)        
            h = R(h, g, u, f, s[C + 14], 15, -1416354905)        
            f = R(f, h, g, u, s[C + 5], 21, -57434055)        
            u = R(u, f, h, g, s[C + 12], 6, 1700485571)        
            g = R(g, u, f, h, s[C + 3], 10, -1894986606)        
            h = R(h, g, u, f, s[C + 10], 15, -1051523)        
            f = R(f, h, g, u, s[C + 1], 21, -2054922799)        
            u = R(u, f, h, g, s[C + 8], 6, 1873313359)        
            g = R(g, u, f, h, s[C + 15], 10, -30611744)        
            h = R(h, g, u, f, s[C + 6], 15, -1560198380)        
            f = R(f, h, g, u, s[C + 13], 21, 1309151649)        
            u = R(u, f, h, g, s[C + 4], 6, -145523070)
            g = R(g, u, f, h, s[C + 11], 10, -1120210379)        
            h = R(h, g, u, f, s[C + 2], 15, 718787259)
            f = R(f, h, g, u, s[C + 9], 21, -343485551)
            u = u + F >> 0
            f = f + dollar >> 0
            h = h + P >> 0
            g = g + _ >> 0
        return Auth.endian([u, f, h, g])

    @staticmethod
    def Get(data):
        i = Auth.MakeStringData(data)
        s = Auth.wordsToBytes(Auth.o(i))
        return Auth.bytesToHex(s).lower()


if __name__ == "__main__":
    MScrawler.Init()

    # 下载英雄卡
    hero_cards = MScrawler.HeroCards()["data"]

    with open(os.path.join(DATA_PATH, "hero_cards.json"), "w", encoding="utf-8") as f:
        f.write(dumps(hero_cards, ensure_ascii=False, indent=4))

    for data in hero_cards:
        hero_detail = MScrawler.HeroCardDetail(int(data['card_id']))["data"]
        with open(os.path.join(HERO_CARDS_PATH, f"{hero_detail['hero_card_info']['card_id']}.json"), "w", encoding="utf-8") as f:
            f.write(dumps(hero_detail, ensure_ascii=False, indent=4))
        with open(os.path.join(HERO_ICON_PATH, f"{hero_detail['hero_card_info']['card_id']}_w.png"), "wb") as f:
            f.write(get(hero_detail['hero_card_info']['icon_url_w']).content)
        with open(os.path.join(HERO_ICON_PATH, f"{hero_detail['hero_card_info']['card_id']}_g.png"), "wb") as f:
            f.write(get(hero_detail['hero_card_info']['icon_url_g']).content)
        
    # 下载支援卡
    support_cards = MScrawler.SupportCards()["data"]

    with open(os.path.join(DATA_PATH, "support_cards.json"), "w", encoding="utf-8") as f:
        f.write(dumps(support_cards, ensure_ascii=False, indent=4))

    for data in support_cards['support_cards']:
        support_card_detail = MScrawler.SupportCardDetail(int(data['card_id']))["data"]
        with open(os.path.join(SUPPORT_CARDS_PATH, f"{data['card_id']}.json"), "w", encoding="utf-8") as f:
            f.write(dumps(support_card_detail, ensure_ascii=False, indent=4))
        with open(os.path.join(SUPPORT_CARDS_PATH, f"{data['card_id']}.png"), "wb") as f:
            f.write(get(data['icon_url']).content)

    # 下载剧本
    script_list = MScrawler.ScriptList()["data"]

    with open(os.path.join(DATA_PATH, "scripts.json"), "w", encoding="utf-8") as f:
        f.write(dumps(script_list, ensure_ascii=False, indent=4))

    for data in script_list:
        script_detail = MScrawler.ScriptDetail(int(data['script_id']))["data"]
        with open(os.path.join(SCRIPT_PATH, f"{data['script_id']}.json"), "w", encoding="utf-8") as f:
            f.write(dumps(script_detail, ensure_ascii=False, indent=4))

