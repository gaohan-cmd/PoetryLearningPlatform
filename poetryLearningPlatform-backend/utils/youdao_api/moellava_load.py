from diffusers import DiffusionPipeline
import torch
import requests
import json

from utils.youdao_api.AuthV3Util import addAuthParams
from utils.gpt.prompt_utils import *
import sys
import os
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
# from AuthV3Util import addAuthParams
# from gpt.prompt_utils import *



from moellava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN
from moellava.conversation import conv_templates, SeparatorStyle
from moellava.model.builder import load_pretrained_model
from moellava.utils import disable_torch_init
from moellava.mm_utils import process_images, tokenizer_image_token, get_model_name_from_path, KeywordsStoppingCriteria

from PIL import Image
from io import BytesIO
from transformers import TextStreamer

# from AuthV3Util import addAuthParams


# 您的应用ID
APP_KEY = ''
# 您的应用密钥
APP_SECRET = ''

# 修改成自己的api key和secret key
APP_KEY = '00a1628544ff1cc0'
# 您的应用密钥
APP_SECRET = 'EhbsXAgBYRUPXt1FZ6APQKyXg4crVkIA'


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
# def get_explain_respond(inputstr):
#     url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()
#     # 注意message必须是奇数条
#     payload = json.dumps({
#         "messages": [
#             {
#                 "role": "user",
#                 "content": inputstr
#             }
#         ],
#         "system": prompt
#     })
#     headers = {
#         'Content-Type': 'application/json'
#     }
#
#     res = requests.request("POST", url, headers=headers, data=payload).json()
#     # 返回处理后的结果
#     return res['result']


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
    model_path = '/work/songyukun/projects/MoE-LLaVA/MoE-LLaVA-StableLM-1.6B-4e'  # LanguageBind/MoE-LLaVA-Qwen-1.8B-4e or LanguageBind/MoE-LLaVA-StableLM-1.6B-4e
    device = 'cuda'
    load_4bit, load_8bit = False, False  # FIXME: Deepspeed support 4bit or 8bit?
    model_name = get_model_name_from_path(model_path)
    tokenizer, model, processor, context_len = load_pretrained_model(model_path, None, model_name, load_8bit, load_4bit,
                                                                     device=device)
    image_processor = processor['image']
    conv_mode = "stablelm"  # phi qwen or stablelm
    conv = conv_templates[conv_mode].copy()
    roles = conv.roles
    image_tensor = image_processor.preprocess(Image.open(image).convert('RGB'), return_tensors='pt')['pixel_values'].to(
        model.device, dtype=torch.float16)

    print(f"{roles[1]}: {english_prompt}")
    inp = DEFAULT_IMAGE_TOKEN + '\n' + english_prompt
    conv.append_message(conv.roles[0], inp)
    conv.append_message(conv.roles[1], None)
    prompt = conv.get_prompt()
    input_ids = tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).cuda()
    stop_str = conv.sep if conv.sep_style != SeparatorStyle.TWO else conv.sep2
    keywords = [stop_str]
    stopping_criteria = KeywordsStoppingCriteria(keywords, tokenizer, input_ids)

    with torch.inference_mode():
        output_ids = model.generate(
            input_ids,
            images=image_tensor,
            do_sample=True,
            temperature=0.2,
            max_new_tokens=1024,
            use_cache=True,
            stopping_criteria=[stopping_criteria])

    outputs = tokenizer.decode(output_ids[0, input_ids.shape[1]:], skip_special_tokens=True).strip()
    print(outputs)
    return outputs


if __name__ == '__main__':
    chinese_prompt = """首句“沙漠的广阔和孤独，烟是烽烟，表示有紧急情况，也说明了当时的环境条件。第二句“长河落日圆”则描绘了长河落日的景象，夕阳西下，河水映照着落日，显得格外美丽。

整首诗语言简练，意象丰富，通过沙漠、河流、烽烟、落日等元素，构建了一幅壮美的画面。"""
    # generate_img(chinese_prompt)

    image = 'moellava/serve/examples/extreme_ironing.jpg'
    inp = 'What is unusual about this image?'
    generate_anwser(inp, image)
