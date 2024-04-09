import torch
import requests
import json
from utils.backend_utils.colorprinter import *
from utils.youdao_api.AuthV3Util import addAuthParams
from utils.gpt.prompt_utils import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
# from AuthV3Util import addAuthParams
# from gpt.prompt_utils import *


from models.moellava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN, DEFAULT_IM_START_TOKEN, \
    DEFAULT_IM_END_TOKEN
from models.moellava.conversation import conv_templates, SeparatorStyle
from models.moellava.model.builder import load_pretrained_model
from models.moellava.utils import disable_torch_init
from models.moellava.mm_utils import process_images, tokenizer_image_token, get_model_name_from_path, \
    KeywordsStoppingCriteria
from PIL import Image
import config
from utils.backend_utils.moellava_model import MOELLAVA_MODEL

# from AuthV3Util import addAuthParams


APP_KEY = config.APP_KEY
APP_SECRET = config.APP_SECRET
APP_KEY_C = config.APP_KEY_C
APP_SECRET_C = config.APP_SECRET_C
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

def createRequest_C(english_prompt):
    '''
    note: 将下列变量替换为需要请求的参数
    '''
    q = english_prompt
    lang_from = 'en'
    lang_to = 'zh-CHS'

    data = {'q': q, 'from': lang_from, 'to': lang_to}

    addAuthParams(APP_KEY_C, APP_SECRET_C, data)

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


def generate_anwser(chinese_prompt, image):
    disable_torch_init()
    # image = '/work/songyukun/projects/PoetryLearningPlatform/poetryLearningPlatform-backend/utils/moellava/serve/examples/desert.jpg'
    # inp = 'What do you see in this image?'
    # chinese_prompt = get_explain_respond(chinese_prompt)
    # ########################
    # # 有道词典翻译提示词
    dict = json.loads(createRequest(chinese_prompt))
    english_prompt = dict["translation"][0]
    print(english_prompt)
    # english_prompt = chinese_prompt
    image_processor = MOELLAVA_MODEL.processor['image']
    conv_mode = "stablelm"  # phi qwen or stablelm
    conv = conv_templates[conv_mode].copy()
    roles = conv.roles
    image_tensor = image_processor.preprocess(Image.open(image).convert('RGB'), return_tensors='pt')['pixel_values'].to(
        MOELLAVA_MODEL.model.device, dtype=torch.float16)
    # print(f"{roles[1]}: {english_prompt}")
    inp = DEFAULT_IMAGE_TOKEN + '\n' + english_prompt
    conv.append_message(conv.roles[0], inp)
    conv.append_message(conv.roles[1], None)
    prompt = conv.get_prompt()
    input_ids = tokenizer_image_token(prompt, MOELLAVA_MODEL.tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).cuda()
    stop_str = conv.sep if conv.sep_style != SeparatorStyle.TWO else conv.sep2
    keywords = [stop_str]
    stopping_criteria = KeywordsStoppingCriteria(keywords, MOELLAVA_MODEL.tokenizer, input_ids)

    with torch.inference_mode():
        output_ids = MOELLAVA_MODEL.model.generate(
            input_ids,
            images=image_tensor,
            do_sample=True,
            temperature=0.2,
            max_new_tokens=1024,
            use_cache=True,
            stopping_criteria=[stopping_criteria])

    outputs = MOELLAVA_MODEL.tokenizer.decode(output_ids[0, input_ids.shape[1]:], skip_special_tokens=True).strip()
    print(outputs)
    dict = json.loads(createRequest_C(outputs))
    chinese_anwser = dict["translation"][0]
    return chinese_anwser


if __name__ == '__main__':
    chinese_prompt = """首句“沙漠的广阔和孤独，烟是烽烟，表示有紧急情况，也说明了当时的环境条件。第二句“长河落日圆”则描绘了长河落日的景象，夕阳西下，河水映照着落日，显得格外美丽。

整首诗语言简练，意象丰富，通过沙漠、河流、烽烟、落日等元素，构建了一幅壮美的画面。"""
    # generate_img(chinese_prompt)

    image = 'moellava/serve/examples/extreme_ironing.jpg'
    inp = 'What is unusual about this image?'
    t = json.loads(createRequest_C(inp))
    generate_anwser(inp, image)
