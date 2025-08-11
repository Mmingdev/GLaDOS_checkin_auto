import requests,json,os
from EncryptClass import Encryptclass
from sendtomp import Send_to_MP
# -------------------------------------------------------------------------------------------
# github workflows
# -------------------------------------------------------------------------------------------
def login_and_get_cookie():
    login_url = "https://ikuuu.de/auth/login"
    headers = {
        "accept":"application/json, text/javascript, */*;",
        "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
        "cookie":"lang=zh-cn",
        "origin":"https://ikuuu.de",
        "priority":"u=1, i",
        "referer":"https://ikuuu.de/auth/login",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }
    data = {
        "host":"ikuuu.de",
        "email": os.environ.get("IKUUU_EMAIL", ""),
        "passwd": os.environ.get("IKUUU_PWD", ""),
        "code":""
    }

    try:
        session = requests.Session()
        response = session.post(login_url, headers=headers, data=data)
        if response.json()['msg'] == '登录成功' and response.status_code == 200 :
            print("登录成功，获取Cookie")
            return session.cookies.get_dict()
        else:
            print("登录失败，状态码：", response.status_code,"信息：",response.json()['msg'])
            return None
    except ConnectionError as e:
        print("代理错误：", e)
        return None
    except Exception as e:
        print("登录过程中发生错误：", e)
        return None

if __name__ == '__main__':
    # 导入系统变量
    sckey = os.environ.get("PUSHPLUS_TOKEN", "")# pushplus秘钥 申请地址 http://www.pushplus.plus/
    APP_ID = os.getenv('APP_ID')
    APP_SECRET = os.getenv('APP_SECRET')
    USER_ID = os.getenv('USER_ID')
    TEMPLATE_ID = os.getenv('TEMPLATE_ID')
    # 推送内容
    sendContent = ''
    # 实例化
    ecmethod = Encryptclass()
    stmp = Send_to_MP(APP_ID,APP_SECRET,USER_ID,TEMPLATE_ID)
    # 账号cookie
    with open('tempdata.txt', 'r', encoding='utf-8') as file:
        d_text = file.read()
    key = os.environ.get("IKUUU_KEY", "")
    cookie = ecmethod.decrypt_oralce(key,d_text)
    # cookie = os.environ.get("ikuuu_COOKIE", "")
    if cookie == "":
        print('未获取到COOKIE')
        exit(0)
    url= "https://ikuuu.de/user/checkin"
    url2= "https://ikuuu.de/user"
    referer = 'https://ikuuu.de/user'
    origin = "https://ikuuu.de"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"

    checkin = requests.post(url,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent,'content-type':'text/html; charset=UTF-8','priority':'u=1, i'})
    if checkin.status_code == 200 and checkin.text.find('msg') != -1:
        msg = checkin.json()['msg']
    else:
        cookie_tm = login_and_get_cookie()
        if cookie_tm != None:
            cookies = cookie_tm.items()
            cookie = 'lang=zh-cn;'
            for name, value in cookies:
                cookie += '{0}={1};'.format(name, value)
            checkin = requests.post(url,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent,'content-type':'text/html; charset=UTF-8','priority':'u=1, i'})
            if checkin.status_code == 200 and checkin.text.find("msg") != -1:
                msg = checkin.json()['msg']
                e_text = Encryptclass.encrypt_oracle(key,cookie)
                with open('tempdata.txt', 'w') as file:
                    file.write(e_text)
            else:
                msg = '签到失败，状态码：{}'.format(checkin.status_code)
        else:
            msg = "登录获取cookie失败"
    print(msg)
    stmp._send_to_mp(msg)
    #--------------------------------------------------------------------------------------------------------#

        #time = state.json()['data']['leftDays']
    #     if isinstance(time,str):
    #         time = time.split('.')[0]
    #     else:
    #         time=str(time)
    #     email = state.json()['data']['email']
    #     if 'message' in checkin.text:
    #         mess = checkin.json()['message']
    #         points = checkin.json()['list'][0]['balance'].split(".")[0]
    #         print(email+'----结果--'+mess+'----剩余('+time+')天'+'----点数('+points+')')  # 日志输出
    #         sendContent += mess+'--剩余('+time+')天'+'--点数('+points+')--'+email+'\n'
    #     else:
    #         requests.get('http://www.pushplus.plus/send?token=' + sckey + '&content='+email+'cookie已失效')
    #         print('cookie已失效')  # 日志输出
    #  #--------------------------------------------------------------------------------------------------------#
    # if sckey != "":
    #      requests.get('http://www.pushplus.plus/send?token=' + sckey + '&title='+email+'签到成功'+'&content='+sendContent)


