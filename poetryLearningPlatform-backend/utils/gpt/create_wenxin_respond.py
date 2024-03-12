import requests
import json
from utils.gpt.prompt_utils import *


# 修改成自己的api key和secret key
API_KEY = "aYqTGFx8T0ynfDZsUMg9QR8p"
SECRET_KEY = "urKh29M5bCAdOBLb5vAW1CCSoHZcic7J"

prompt = get_prompt_zn()


# 获取回复
def get_explain_respond(inputstr):
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
    return (res['result'])


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    get_explain_respond()
