import base64
import json
import requests
import time
import os

img_path="qrcode_temp.png"
def base64_api(uname="Zion", pwd="123456qwerty", img=img_path):
    with open(img, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]


if __name__ == "__main__":
    result = base64_api()
    print(result)