from flask import Blueprint, jsonify
import flask
from utils.backend_utils.dir_utils import *
from utils.backend_utils.colorprinter import *
from utils.gpt.create_wenxin_respond import *
from utils.youdao_api.playground_load import *
from poem_backend import *
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

bp = Blueprint(name='poem', import_name=__name__)


@bp.route("/search/poem", methods=['GET'])
@swag_from('swagger_yml/poem/search_poem.yml')
def search_poem_controller():
    args = dict(flask.request.args)
    query_str = args['query_str']
    query_type = args['query_type']
    items_per_page = int(args.get('items_per_page', 100))
    curr_page = int(args.get('curr_page', 1))

    return jsonify(search_poem(query_str, query_type, items_per_page, curr_page))


@bp.route("/search/poem_cloud", methods=['GET'])
@swag_from('swagger_yml/poem/search_poem_cloud.yml')
def search_poem_cloud_controller():
    args = dict(flask.request.args)
    query_str = args['query_id']
    query_type = args['query_type']
    items_per_page = int(args.get('items_per_page', 1000))
    curr_page = int(args.get('curr_page', 1))

    return jsonify(search_poem_cloud(query_str, query_type, items_per_page, curr_page))


@bp.route("/query/poem_by_id", methods=['GET'])
@swag_from('swagger_yml/poem/query_poem_by_id.yml')
def query_poem_by_id_controller():
    args = dict(flask.request.args)
    p_id = int(args['p_id'])

    return jsonify(query_poem_by_id(p_id))


@bp.route("/search/author", methods=['GET'])
@swag_from('swagger_yml/poem/search_author.yml')
def search_author_controller():
    args = dict(flask.request.args)
    query_str = args['query_str']
    items_per_page = int(args.get('items_per_page', 100))
    curr_page = int(args.get('curr_page', 1))

    return jsonify(search_author(query_str, items_per_page, curr_page))


@bp.route("/query/poem_by_author", methods=['GET'])
@swag_from('swagger_yml/poem/query_poem_by_author.yml')
def query_poem_by_author_controller():
    args = dict(flask.request.args)
    a_id = args['a_id']
    items_per_page = int(args.get('items_per_page', 100))
    curr_page = int(args.get('curr_page', 1))

    return jsonify(query_poem_by_author(a_id, items_per_page, curr_page))


@bp.route("/display/author", methods=['GET'])
@swag_from('swagger_yml/poem/display_author.yml')
def display_author_controller():
    args = dict(flask.request.args)
    items_per_page = int(args.get('items_per_page', 100))
    return jsonify(display_author(items_per_page))


@bp.route("/display/rhythmic", methods=['GET'])
@swag_from('swagger_yml/poem/display_rhythmic.yml')
def display_rhythmic_controller():
    args = dict(flask.request.args)
    items_per_page = int(args.get('items_per_page', 100))

    return jsonify(display_rhythmic(items_per_page))


@bp.route("/search/rhythmic", methods=['GET'])
@swag_from('swagger_yml/poem/search_rhythmic.yml')
def search_rhythmic_controller():
    args = dict(flask.request.args)
    r_name = args['r_name']
    items_per_page = int(args.get('items_per_page', 100))
    curr_page = int(args.get('curr_page', 1))

    return jsonify(search_rhythmic(r_name, items_per_page, curr_page))


@bp.route("/query/poem_by_rhythmic", methods=['GET'])
@swag_from('swagger_yml/poem/query_poem_by_rhythmic.yml')
def query_poem_by_rhythmic_controller():
    args = dict(flask.request.args)
    r_id = int(args['r_id'])
    items_per_page = int(args.get('items_per_page', 100))
    curr_page = int(args.get('curr_page', 1))

    return jsonify(query_poem_by_rhythmic(r_id, items_per_page, curr_page))


@bp.route("/display/collection", methods=['GET'])
@swag_from('swagger_yml/poem/display_collection.yml')
def display_collection_controller():
    return jsonify(display_collection())


@bp.route("/query/poem_by_collection", methods=['GET'])
@swag_from('swagger_yml/poem/query_poem_by_collection.yml')
def query_poem_by_collection_controller():
    args = dict(flask.request.args)
    c_id = int(args['c_id'])
    items_per_page = int(args.get('items_per_page', 100))
    curr_page = int(args.get('curr_page', 1))

    return jsonify(query_poem_by_collection(c_id, items_per_page, curr_page))


@bp.route("/query/random_poem", methods=['GET'])
@swag_from('swagger_yml/poem/query_random_poem.yml')
def query_random_poem_controller():
    return jsonify(query_random_poem())
