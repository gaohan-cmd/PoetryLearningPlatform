

import requests
import json
from AuthV3Util import addAuthParams

# 您的应用ID
APP_KEY = '00a1628544ff1cc0'
# 您的应用密钥
APP_SECRET = 'Zhs4yuNZAkRnYv6ObvwQtymHVjfPvTVR'


def createRequest(chinese_prompt):
    '''
    note: 将下列变量替换为需要请求的参数
    '''
    q = chinese_prompt
    lang_from = 'zh-CHS'
    lang_to = 'en'

    data = {'q': q, 'from': lang_from, 'to': lang_to}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/api', header, data, 'post')
    return str(res.content, 'utf-8')


def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header)


def getEnglishPrompt(chinese_prompt):
    dict = json.loads(createRequest(chinese_prompt))
    english_prompt = dict["translation"]
    print(english_prompt)


if __name__ == '__main__':
    chinese_prompt = "白日依山尽，黄河入海流"
    getEnglishPrompt(chinese_prompt)