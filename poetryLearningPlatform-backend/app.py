import sqlalchemy
import torch

import config
import argparse
import os

from flask import Flask, g, session, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, get_jwt

from extensions import *
from utils.backend_utils.colorprinter import *
from database_models import *
from blueprints.auth_bp import bp as auth_bp
from blueprints.server_bp import bp as server_bp
from blueprints.user_manage_bp import bp as user_manage_bp
from blueprints.chat_bp import bp as chat_bp
from blueprints.poem_bp import bp as poem_bp
from flasgger import Swagger
import os
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

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
jwt = JWTManager(app)
mail.init_app(app)
'''
flask db init
flask db migrate
flask db upgrade
'''
migrate = Migrate(app, db)
Swagger(app)
app.config['JSON_AS_ASCII'] = False
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(server_bp, url_prefix='/server')
app.register_blueprint(user_manage_bp, url_prefix='/user-manage')
# 文生图模型-生成图片-回答文本-图文对话
app.register_blueprint(chat_bp, url_prefix='/chat')
app.register_blueprint(poem_bp, url_prefix='/poem')


# 注册一个函数，该函数在第一次请求之前运行
@app.before_first_request
def load_default_model():
    g.repo_dir = repo_dir
    session['repo_dir'] = g.repo_dir


# 注册一个函数，该函数在每次请求之前运行
# @app.before_request
# def before_request():


def test_database_connection():
    with app.app_context():
        with db.engine.connect() as conn:
            res = conn.execute(sqlalchemy.text('select 1'))
            if res.fetchone()[0] == 1:
                print_green('Database connection successful')
            else:
                print_red('Database connection failed')

from diffusers import DiffusionPipeline
import torch
import requests
import json
from utils.youdao_api.AuthV3Util import addAuthParams
from utils.gpt.prompt_utils import *
from models.moellava.mm_utils import get_model_name_from_path
from models.moellava.model.builder import load_pretrained_model


if __name__ == "__main__":
    repo_dir = os.getcwd()
    parser = argparse.ArgumentParser(description="Flask app exposing poetry learning platform API")
    parser.add_argument("--port", default=5003, type=int, help="port number")
    parser.add_argument("--local_rank", default=0, type=int, help="--")
    args = parser.parse_args()
    test_database_connection()
    print_cyan('项目已启动')
    print_cyan(f'当前工作目录: {repo_dir}')
    app.run(host="0.0.0.0", port=args.port, debug=True)

