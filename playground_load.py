from diffusers import DiffusionPipeline
import torch

pipe = DiffusionPipeline.from_pretrained(
    "/home/sjc/Program/playground-v2-512px-base",
    torch_dtype=torch.float16,
    use_safetensors=True,
    add_watermarker=False,
    variant="fp16",
)
pipe.to("cuda")

chinese_prompt = "月黑见渔灯，孤光一点萤"

import requests
import json
from apidemo.utils.AuthV3Util import addAuthParams

# 您的应用ID
APP_KEY = ''
# 您的应用密钥
APP_SECRET = ''


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

dict = json.loads(createRequest(chinese_prompt))
english_prompt = dict["translation"]

prompt = "{},8k".format(english_prompt[0])

image = pipe(prompt=prompt, width=512, height=512).images[0]

image.save("")
