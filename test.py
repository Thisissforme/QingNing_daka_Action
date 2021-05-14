import requests
# 酷推机器人
def kutui():
    url = "https://push.xuthus.cc/group/848c8ac61b3d42195673ab57bcf51cf7"
    data='小王打卡失败@face=67@'
    da=data.encode('utf-8')
    requests.post(url, da)
kutui()