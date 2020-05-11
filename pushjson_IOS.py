import re
import json
import sys
import time
from translate import GoogleTrans
sys.path.append(r'./translate.py')

def openfile(sentence_IOS, language):
    with open('../IOS版本词条/iOS_Dictionary/' + language + '.lproj/Localizable.strings', 'r', encoding='utf-8') as txt:
        list_one = txt.readlines()
        print(len(list_one))
        print(list_one[len(list_one) - 1])
        list_one[len(list_one) - 1] = str(list_one[len(list_one) - 1]) + "\n"
        print(list_one)
    list_one.append(sentence_IOS)
    print(list_one)
    with open('../IOS版本词条/iOS_Dictionary/' + language + '.lproj/Localizable.strings', 'w', encoding='utf-8') as f:
        f.write(''.join(list_one))

def IOS_citiao():
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
        print(en)
        sentence_IOS = '"' + "".join(en) + '" = "' + "".join(load_dict[keys[i]]) + '";'
        print(sentence_IOS)
        keys[i] = keys[i].replace("_"+str(n), "")
        if keys[i] == 'zh-TW':
            openfile(sentence_IOS, 'zh-Hant')
            openfile(sentence_IOS, 'zh-HK')
        elif keys[i] == 'zh-CN':
            openfile(sentence_IOS, 'zh-Hans')
        else:
            openfile(sentence_IOS, keys[i])

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
    IOS_citiao()