import requests
import sys
import time
import json
import xlrd
from selenium import webdriver
import os
import base64
headers={
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    }
url1 = ' https://wxyqfk.zhxy.net/?yxdm=10623#/login'
url2 = 'https://wxyqfk.zhxy.net/?yxdm=10623#/clockIn'


def login():
    global data_login
    data_login={
        "Name": stu_name,
        "PassWord": stu_sign_password,
        "UserType": "1",
        "XGH": stu_xgh,
        "YXDM": "10623"
        }
    login_url = "https://wxyqfk.zhxy.net/?yxdm=10623#/login"
    # 登陆
    s=requests.Session()
    s.post(login_url, data=data_login, headers=headers)
    # post登陆页面
    login_result=s.post("https://yqfkapi.zhxy.net/api/User/CheckUser")
    print(login_result)
    return s

'''
图像识别接口一 http://www.fateadm.com/ 已舍弃，太贵了
'''
def get_qrcode():
    pass

'''
图像识别接口2 http://www.ttshitu.com/
'''
def get_qrcode2():
    pic1=requests.get('https://yqfkapi.zhxy.net/api/common/getverifycode')
    tex1=pic1.content
    tex2=bytes.decode(tex1)
    if json.loads(tex2)['info'] == '非法访问！':
        print(tex2)
        sys.exit()
    tex3=json.loads(tex2)['data']['img']
    key=json.loads(tex2)['data']['key']
    url='data:image/png;base64,'+tex3
    # print(url)
    # print(qr_key)
    # 1.识别验证码
    img_url = url
    from tujian import base64_api
    from urllib.request import urlretrieve
    urlretrieve(img_url, 'qrcode_temp.png')
    time.sleep(2)
    code = base64_api()
    # code="1234"
    print("调用了2接口（图鉴接口）")
    return key,code



# 创建日志，清除日志内容
def recoding_clean():
    with open("recoding.txt", 'w+') as f:
        f.read()
    with open("recoding.txt", 'r+') as f:
        f.seek(0)
        f.truncate()  # 清空文件


def kutui(stu_name):
    KUTUIkey= os.environ["KUTUIkey"]
    url = "https://push.xuthus.cc/group/"+KUTUIkey
    data=stu_name+'打卡失败了，手动打吧@face=67@'
    da=data.encode('utf-8')
    requests.post(url, da)

# 运行成功写入1,
def recoding_ture():
    with open("recoding.txt", 'a+') as f:
        state="1,"
        f.write(state)


# 运行失败写入0,
def recoding_false():
    with open("recoding.txt", 'a+') as f:
        state="0,"
        f.write(state)


def health_daka(s,key,code):
    data_health={
        "UID":stu_uid,
        "UserType":"1",
        "JWD":JWD,
        "key":key,
        "code":code,
        "ZZDKID":"37",
        "A1":"正常",
        "A4":"无",
        "A2":"全部正常",
        "A3":Place,
        "A11":"在校",
        "A12":"未实习",
        "YXDM":"10623",
        "version":"v1.3.2"
    }
    # for i in range(2):
    health_url = 'https://wxyqfk.zhxy.net/?yxdm=10623#/clockIn'
    s.post(health_url,headers=headers)
    s.post('https://yqfkapi.zhxy.net/api/ClockIn/Save',data=data_health,headers=headers)


def webdriver_holdon():
    path = "chromedriver"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.get("https://wxyqfk.zhxy.net/?yxdm=10623#/login")
    time.sleep(2)
    XGH = driver.find_elements_by_class_name('van-field__body')[0].find_element_by_tag_name('input')
    XGH.send_keys(data_login['XGH'])
    Name = driver.find_elements_by_class_name('van-field__body')[1].find_element_by_tag_name('input')
    Name.send_keys(data_login['Name'])
    Password = driver.find_elements_by_class_name('van-field__body')[3].find_element_by_tag_name('input')
    Password.send_keys(data_login['PassWord'])
    time.sleep(1)
    login_button = driver.find_element_by_class_name('sign-in-btn')
    login_button.click()
    time.sleep(2)
    driver.get("https://wxyqfk.zhxy.net/?yxdm=10623#/clockIn")
    time.sleep(1)
    return driver

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


if __name__ == '__main__':
    position = 0
    recoding_clean()
    book = xlrd.open_workbook("data.xls")
    table = book.sheet_by_name("data")
    # 获取总行数总列数
    row_Num = table.nrows
    col_Num = table.ncols
    lis = []
    j = 1
    key = table.row_values(0)  # 这是第一行数据，作为字典的key值
    for i in range(row_Num - 1):
        data = {}
        values = table.row_values(j)
        for x in range(col_Num):
            # 把key值对应的value赋值给key，每行循环
            data[key[x]] = values[x]
        j += 1
        # 把字典加到列表中
        lis.append(data)
    for i in lis:
        a="fall"
        stu_name = str(i['stu_name'])
        stu_password = str(i['stu_password'])  # 加密后的密码
        stu_xgh = str(i['stu_xgh'])
        stu_uid = str(int(i['stu_uid']))
        JWD = str(i['JWD'])
        Place = str(i['Place'])
        phone = str(int(i['phone']))
        stu_sign_password=str(i['password'])  # 登录密码
        # print(stu_name, stu_password, stu_xgh, stu_uid, JWD, Place)
        s = login()
        driver = webdriver_holdon()
        # 检测是否打卡
        try:
            # time.sleep(2)
            print("检测打卡状态")
            if driver.find_element_by_class_name('already-title cc_cursor'):
                print(stu_name+"今天已打卡")
                driver.close()
                a="success"
            else:
                print("未打卡，刷新重新检查")
                driver.refresh()
                driver.find_element_by_class_name("already-title cc_cursor")
                print(stu_name + "今天已打卡")
                driver.close()
                a="success"
        # 识别验证码
        except:
            print("未打卡，开始打卡------")
            key, code = get_qrcode2()
            print(code)
            time.sleep(2)
            health_daka(s, key, code)
            if len(code)==4:
                a = "sucess"
            else:
                a="wrong"
            driver.close()
        time.sleep(3)
        # 记录日志
        if a=="success":
            print(stu_name+"打卡成功")
            recoding_ture()
        else:
            print(stu_name+"打卡失败")
            recoding_false()
    sys.exit()