import requests
import sys
import time
import json
import xlrd
from selenium import webdriver
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
图像识别接口一 http://www.fateadm.com/
'''
def get_qrcode():
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
    from get_code import TestFunc
    from urllib.request import urlretrieve
    urlretrieve(img_url, 'qrcode_temp.png')
    code = TestFunc()
    # code="1234"
    print(code)
    print("调用了1接口（斐斐打码接口）")
    return key,code

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

# 钉钉机器人(已放弃）
def send_msg(text,atphone):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    url = 'https://oapi.dingtalk.com/robot/send?access_token=cfb45651fad634745c979270b807f07d3a083e9ce35e0d4776adbf069126b113'
    json_text = {
        "msgtype":"text",
        "text": {
            "content": ""
        },
        "at": {
            "atMobiles": atphone,
            "isAtAll": False
        }
    }
    json_text['text']['content']=text
    json_text['at']['atMobiles']=atphone
    requests.post(url, json.dumps(json_text), headers=headers)


# 酷推机器人
# 酷推机器人
def kutui(stu_name):
    url = "https://push.xuthus.cc/group/848c8ac61b3d42195673ab57bcf51cf7"
    data=stu_name+'打卡失败了，手动打吧@face=67@'
    da=data.encode('utf-8')
    requests.post(url, da)

# 创建日志，清除日志内容
def recoding_clean():
    with open("recoding.txt", 'w+') as f:
        f.read()
    with open("recoding.txt", 'r+') as f:
        f.seek(0)
        f.truncate()  # 清空文件


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

if __name__ == '__main__':
    # 查看日志记录值
    position = 0
    recoding_list = [] # 记录值
    with open("recoding.txt",'r') as f:
        recoding_data = f.read()
        for i in recoding_data:
            if i == ",":
                continue
            else:
                recoding_list.append(int(i))
    ## 打开数据表
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
        if recoding_list[position]==1:
            position+=1
            print(str(i['stu_name'])+"已打卡")
            continue
        else:
            position+=1
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
            try:
                # time.sleep(2)
                if driver.find_element_by_class_name('already-title'):
                    print(stu_name+"今天已打卡")
                    driver.close()
                    a="success"
                else:
                    time.sleep(2)
                    driver.refresh()
                    driver.find_element_by_class_name("already-title")
                    print(stu_name + "今天已打卡")
                    a = "success"
                    driver.close()
            except:
                key, code = get_qrcode2()
                time.sleep(2)
                health_daka(s, key, code)
                if len(code)==4:
                    a="success"
                else:
                    a='wrong'
                driver.close()
            time.sleep(2)
            # 简单的验证
            if a=="success":
                with open("recoding.txt",'w') as f:
                    recoding_list[position-1]=1
                    for i in recoding_list:
                        f.write(str(i)+',')
                print(stu_name+"打卡成功")
            else:
                # 发送消息
                print(stu_name+"打卡失败")
                txt=":打卡失败"+stu_name
                a=time.strftime("%H", time.localtime())# 当前时间
                if int(a)>=6:
                    kutui(stu_name)
    sys.exit()