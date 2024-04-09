from utils.backend_utils.colorprinter import *
import requests
import json
from utils.gpt.prompt_utils import *
from utils.youdao_api.AuthV3Util import addAuthParams
import config
from utils.backend_utils.diffusion_model import pipe

APP_KEY = config.APP_KEY
APP_SECRET = config.APP_SECRET
API_KEY = config.API_KEY
SECRET_KEY = config.SECRET_KEY


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


prompt = get_prompt_pic()


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


# 获取回复
def get_explain_respond_poem(inputstr):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()
    # 注意message必须是奇数条
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": inputstr
            }
        ],
        "system": prompt
    })
    headers = {
        'Content-Type': 'application/json'
    }

    res = requests.request("POST", url, headers=headers, data=payload).json()
    # 返回处理后的结果
    return res['result']


def generate_img(chinese_prompt):
    chinese_prompt = get_explain_respond_poem(chinese_prompt)
    # 有道词典翻译提示词
    dict = json.loads(createRequest(chinese_prompt))
    english_prompt = dict["translation"]
    print(english_prompt)
    prompt = "An ultra realistic photo taken with a canon eos r5 camera,{}".format(english_prompt)
    image = pipe.model(prompt=prompt, width=512, height=512).images[0]

    # 图片保存
    image.save("image.png")
    return image


if __name__ == '__main__':
    chinese_prompt = """首句“沙漠的广阔和孤独，烟是烽烟，表示有紧急情况，也说明了当时的环境条件。第二句“长河落日圆”则描绘了长河落日的景象，夕阳西下，河水映照着落日，显得格外美丽。

整首诗语言简练，意象丰富，通过沙漠、河流、烽烟、落日等元素，构建了一幅壮美的画面。"""
    generate_img(chinese_prompt)

    # image = 'moellava/serve/examples/extreme_ironing.jpg'
    # inp = 'What is unusual about this image?'
    # generate_anwser(inp, image)
