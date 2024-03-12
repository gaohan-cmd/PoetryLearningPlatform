import requests
import json


def main():
    # client id = API Key, client_secret = Secret Key 修改成自己的API Key 和Sercet Key
    client_id = "4YqbzGV59w6BU3Hh1GlBsaA1"
    client_secret = "3mM6ys4yAG5j******v"
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=aYqTGFx8T0ynfDZsUMg9QR8p&client_secret=urKh29M5bCAdOBLb5vAW1CCSoHZcic7J"

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

if __name__ == '__main__':
    main()

# 会再终端打印一行文本即acess token