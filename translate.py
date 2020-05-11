#! /usr/bin/env python
# -*- coding:utf-8 -*-
# rate: 1
# burst: 312

import urllib.request
import urllib.parse
import json
import execjs
import re
import ssl
import time

ssl._create_default_https_context = ssl._create_unverified_context


class GoogleTrans(object):
    def __init__(self):
        self.url = 'https://translate.google.cn/translate_a/single'
        self.TKK = "434674.96463358"  # 随时都有可能需要更新的TKK值

        self.header = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": "NID=200=IvKh47Cs3X-CwjwFNJceDmRE7vzy4UcWTiUgcQZlFxfcftWkIJnKFZVHHCOGHpeeCwtYuyxiu_EwYSaTXbOJNOWMUTAngY9hfFGdt7jtD-DKuMX6-wjOGmdtr-ts3y5fYQkBBxWcb3Lsug2WHrXvPogBx7mk9Q6S5946IpoXW7M",
            "referer": "https://translate.google.cn/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
            "x-client-data": "CIe2yQEIpLbJAQjEtskBCKmdygEItqDKAQjQr8oBCLywygEI7bXKAQiOusoBGJu+ygE=",
        }

        self.data = {
            "client": "webapp",  # 基于网页访问服务器
            "sl": "auto",  # 源语言,auto表示由谷歌自动识别
            "tl": "vi",  # 翻译的目标语言
            "hl": "zh-CN",  # 界面语言选中文，毕竟URL都是cn后缀了，就不装美国人了
            "dt": ["at", "bd", "ex", "ld", "md", "qca", "rw", "rm", "ss", "t"],  # dt表示要求服务器返回的数据类型
            "otf": "2",
            "ssel": "0",
            "tsel": "0",
            "kc": "1",
            "tk": "",  # 谷歌服务器会核对的token
            "q": "",  # 待翻译的字符串
            "language": ["ar", "hi", "vi", "de", "fr", "ru", "es", "id", "ja", "ko", "th", "zh-TW"]
        }

        with open('token.js', 'r', encoding='utf-8') as f:
            self.js_fun = execjs.compile(f.read())

        # 构建完对象以后要同步更新一下TKK值
        # self.update_TKK()

    def update_TKK(self):
        url = "https://translate.google.cn/"
        req = urllib.request.Request(url=url, headers=self.header)
        page_source = urllib.request.urlopen(req).read().decode("utf-8")
        self.TKK = re.findall(r"tkk:'([0-9]+\.[0-9]+)'", page_source)[0]

    def construct_url(self):
        base = self.url + '?'
        for key in self.data:
            if isinstance(self.data[key], list):
                base = base + "dt=" + "&dt=".join(self.data[key]) + "&"
            else:
                base = base + key + '=' + self.data[key] + '&'
        base = base[:-1]
        return base

    def query(self, q, lang_to=''):
        self.data['q'] = urllib.parse.quote(q)
        self.data['tk'] = self.js_fun.call('wo', q, self.TKK)
        self.data['tl'] = lang_to
        url = self.construct_url()
        req = urllib.request.Request(url=url, headers=self.header)
        time.sleep(20)
        response = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
        targetText = response[0][0][0]
        originalText = response[0][0][1]
        originalLanguageCode = response[2]
        print("翻译前：{}，翻译前code：{}".format(originalText, originalLanguageCode))
        print("翻译后：{}, 翻译后code：{}".format(targetText, lang_to))
        return (format(originalText), format(originalLanguageCode), format(targetText), format(lang_to))

    def writejson(self, q, n):
        translate_to = {}
        for i in range(len(self.data['language'])):
            print(i)
            print(self.data['language'][i])
            originalText, originalLanguageCode, targetText, lang_to = self.query(q, lang_to=self.data['language'][i])
            print(originalText)
            print(originalLanguageCode)
            print(targetText)
            print(lang_to)
            if i == 0:
                translate_to = {"".join(format(originalLanguageCode)) + "_" + str(n): format(originalText)}
            translate = {"".join(format(lang_to)) + "_" + str(n): format(targetText)}
            translate_to.update(translate)
            print(translate_to)
            if n == 1:
                file_name = time.strftime("citiao%Y-%m-%d", time.localtime())
                jsontext = json.dumps(translate_to, ensure_ascii=False, sort_keys=False, indent=4)
                with open('./词条/%s.json' % file_name, 'w', encoding='utf-8') as txt:
                    txt.write(jsontext)
            elif n >= 2:
                file_name = time.strftime("citiao%Y-%m-%d", time.localtime())
                with open('./词条/%s.json' % file_name, 'r', encoding='utf-8') as txt:
                    citiao_dict = json.load(txt)
                    print(citiao_dict)
                citiao_dict.update(translate_to)
                with open('./词条/%s.json' % file_name, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(citiao_dict, ensure_ascii=False, sort_keys=False, indent=2))
            # time.sleep(10)  # Delay for 1 minute (60 seconds).