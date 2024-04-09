from flask import Blueprint, request
from PIL import Image
import base64
from io import BytesIO
from utils.backend_utils.dir_utils import *
from utils.backend_utils.response_utils import response
from utils.backend_utils.colorprinter import *
from utils.gpt.create_wenxin_respond import *
from utils.youdao_api.playground_load import *
from utils.youdao_api.moellava_load import *
from flasgger import swag_from

'''
前后端code约定：
code: 0 成功 前端无消息弹窗
code: 1 失败 前端无消息弹窗
code: 200 前端消息弹窗Success
code: 201 前端消息弹窗Error
code: 202 前端消息弹窗Warning
code: 203 前端消息弹窗Info
code: 204 前端通知弹窗Success
code: 205 前端通知弹窗Error
code: 206 前端通知弹窗Warning
code: 207 前端通知弹窗Info
'''

bp = Blueprint(name='chat', import_name=__name__)


@bp.route('/generate/wenxin', methods=['POST'])
@swag_from('swagger_yml/chat/generate_wenxin.yml')
# @jwt_required(refresh=True)
def generateByWenXin():
    # 对诗词内容进行讲解
    poetryContent = request.json.get('poetryContent', '').strip()

    data = {
        'poetryExplain': get_explain_respond(poetryContent),
    }
    return response(code=0, message='回答成功', data=data)


@bp.route('/generate/playground', methods=['POST'])
@swag_from('swagger_yml/chat/generate_playground.yml')
def generate_image_playground():
    # 对诗词内容生成图片
    chinese_prompt = request.json.get('poetryContent', '').strip()
    original_base64 = generate_image(chinese_prompt)

    response_data = {
        'originalBase64': original_base64
    }
    return response(code=0, message='图片生成已完成', data=response_data)


@bp.route('/generate/moellava', methods=['POST'])
@swag_from('swagger_yml/chat/generate_moellava.yml')
# def generate_anwsers_playground(chinese_prompt, image):
def generate_moellava_anwsers():
    # 获取前端的中文问题 + youdao_api路径下读取的图片，返回回答的文字
    chinese_prompt = request.json.get('poetryQuestion', '').strip()
    image = "utils/youdao_api/image.png"  # 在哪里加载图片
    answer = generate_anwser(chinese_prompt, image)
    response_data = {
        'answer': answer
    }
    return response(code=0, message='回答已生成', data=response_data)


def generate_image(chinese_prompt):
    # 调用模型接口生成图片
    results = generate_img(chinese_prompt)

    img_bytes = BytesIO()
    results.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    original_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
    return original_base64


# base64编码生成的图片
def batch_base64_encode_image(results_images):
    for im in results_images.imgs:
        buffered = BytesIO()
        im_base64 = Image.fromarray(im)
        im_base64.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')
