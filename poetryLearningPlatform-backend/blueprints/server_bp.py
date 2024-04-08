from flask import Blueprint, session
from utils.backend_utils.response_utils import response
from utils.backend_utils.colorprinter import *
from flasgger import swag_from

bp = Blueprint('server', __name__, url_prefix='/server')


# 查看服务端Session
@bp.route('/session/list', methods=['GET'])
@swag_from('swagger_yml/server/session_list.yml')
def session_data():
    print_cyan(session)
    return response(code=200, data=session, message='获取session成功')


# 清除服务端Session
@bp.route('/session/clear')
@swag_from('swagger_yml/server/session_clear.yml')
def logout():
    session.clear()
    return response(code=200, message='清除session成功')
