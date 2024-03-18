import os
from pprint import pprint

from flask import Blueprint, request, render_template, g, redirect, session
from PIL import Image
import datetime
import base64

from io import BytesIO
from flask_jwt_extended import jwt_required
from database_models import WeightsModel
from utils.backend_utils.dir_utils import *
from utils.backend_utils.response_utils import response
from utils.backend_utils.colorprinter import *
from utils.gpt.create_wenxin_respond import *
from utils.youdao_api.playground_load import *

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

DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S-%f"


@bp.route('/weights/current')
@jwt_required(refresh=True)
def get_current_weights():
    weights_path = session['weights_path']
    current_weights = WeightsModel.query.filter_by(weights_relative_path=weights_path).first()
    weights_name = current_weights.weights_name
    weights_version = current_weights.weights_version
    data = {
        'weightsName': weights_name,
        'weightsVersion': weights_version,
    }
    return response(code=0, message='获取当前调用权重成功', data=data)


@bp.route('/weights/list')
@jwt_required(refresh=True)
def get_all_enable_weights():
    all_enable_weights = []
    weights_models = WeightsModel.query.filter_by(enable=True).all()
    for weights_model in weights_models:
        all_enable_weights.append({
            'weightsName': weights_model.weights_name,
            'weightsVersion': weights_model.weights_version
        })
    data = {'list': all_enable_weights}
    return response(code=0, message='获取所有可调用权重成功', data=data)


def print_cyan(param):
    print(param)


@bp.route('/weights/switch', methods=['POST'])
@jwt_required(refresh=True)
def switch_weights():
    weights_name = request.json.get('switchWeightsName', '').strip()
    weights_version = request.json.get('switchWeightsVersion', '').strip()
    repo_dir = session['repo_dir']
    new_weights = WeightsModel.query.filter_by(weights_name=weights_name,
                                               weights_version=weights_version).first()
    if new_weights and new_weights.enable:
        new_weights_path = new_weights.weights_relative_path
        new_weights_name = new_weights.weights_name
        new_weights_version = new_weights.weights_version
        model_load_path = os.path.join(repo_dir, new_weights_path)
        print_cyan(f'切换成功，当前调用权重：{new_weights_name}，权重版本{weights_version}')
        session['repo_dir'] = repo_dir
        session['weights_path'] = new_weights_path
        session['model_load_path'] = model_load_path
        session['weights_name'] = new_weights_name
        data = {
            'weightsName': new_weights_name,
            'weightsVersion': new_weights_version,
        }
        return response(code=200, message='切换模型成功', data=data)
    elif not new_weights:
        return response(code=201, message='切换模型失败，当前模型不存在')
    else:
        return response(code=201, message='切换模型失败，当前模型暂不可用')


@bp.route('/generate/wenxin', methods=['POST'])
# @jwt_required(refresh=True)
def generateByWenXin():
    # 对诗词内容进行讲解
    poetryContent =request.json.get('poetryContent', '').strip()

    data = {
        'poetryExplain': get_explain_respond(poetryContent),
    }
    return response(code=0, message='回答成功', data=data)

@bp.route('/generate/playground', methods=['POST'])
def generate_image_playground():
    # 对诗词内容生成图片
    chinese_prompt = request.json.get('poetryContent', '').strip()
    original_base64 = generate_image(chinese_prompt)

    response_data = {
        'originalBase64': original_base64
    }
    return response(code=0, message='图片生成已完成', data=response_data)


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