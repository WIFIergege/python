from docx import Document
import re
import json
import sys
import time
from translate import GoogleTrans
sys.path.append(r'./translate.py')

def enselct( en ):
    en = "".join(en)
    en = en.replace(" ", "_")
    en = en.replace("!", "")
    en = en.replace("###_", "")
    en = en.replace(".", "")
    en = en.replace("’", "")
    en = en.replace("😉", "")
    en = en.replace("…", "")
    en = en.replace("?", "")
    en = en.replace("?", "")
    en = en.replace("?", "")
    en = en.replace("?", "")
    en = en.replace("?", "")
    en = en.lower()
    return en

def Android_citiao():
    file_name = time.strftime("citiao%Y-%m-%d", time.localtime())
    with open('./词条/%s.json' % file_name, 'r', encoding='utf-8') as txt:
        load_dict = json.load(txt)
        print(load_dict)
    keys = list(load_dict.keys())
    print(keys)
    for i in range(len(keys)):
        print(keys[i])
        n = i//14+1
        print(n)
        en = load_dict['en_'+str(n)]
        en = enselct(en)
        print(en)
        sentence_Android = {en: load_dict[keys[i]]}
        print(sentence_Android)
        keys[i] = keys[i].replace("_"+str(n), "")
        with open('../安卓版本词条/安卓改版词条/val_' + keys[i] + '.json', 'r', encoding='utf-8') as txt:
            citiao_dict = json.load(txt)
            print(citiao_dict)
        citiao_dict.update(sentence_Android)
        print(citiao_dict)
        with open('../安卓版本词条/安卓改版词条/val_' + keys[i] + '.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(citiao_dict, ensure_ascii=False, sort_keys=False, indent=2))

if __name__ == '__main__':
    translate_text = ["Hello world", "hi"]
    text = {"zh-CN_1": "你好，世界", "zh-CN_2": "你好"}
    n = 0
    for i in range(len(translate_text)):
        n = n + 1
        GoogleTrans().writejson(translate_text[i], n)
        keys = list(text.keys())
        print(keys)
        sentence_Android = {keys[i]: text[keys[i]]}
        file_name = time.strftime("citiao%Y-%m-%d", time.localtime())
        with open('./词条/%s.json' % file_name, 'r', encoding='utf-8') as txt:
            load_dict = json.load(txt)
            print(load_dict)
        load_dict.update(sentence_Android)
        with open('./词条/%s.json' % file_name, 'w', encoding='utf-8') as f:
            f.write(json.dumps(load_dict, ensure_ascii=False, sort_keys=False, indent=2))
    Android_citiao()
