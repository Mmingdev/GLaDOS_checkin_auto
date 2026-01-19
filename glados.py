import requests,json,os
# -------------------------------------------------------------------------------------------
# github workflows
# -------------------------------------------------------------------------------------------
if __name__ == '__main__':
# pushplus秘钥 申请地址 http://www.pushplus.plus/
    sckey = os.environ.get("PUSHPLUS_TOKEN", "")
# 推送内容
    sendContent = ''
# glados账号cookie 直接使用数组 如果使用环境变量需要字符串分割一下
    cookies = os.environ.get("GLADOS_COOKIE", []).split("&")
    if cookies[0] == "":
        print('未获取到COOKIE变量') 
        cookies = []
        exit(0)
    url= "https://glados.cloud/api/user/checkin"
    url2= "https://glados.cloud/api/user/status"
    referer = 'https://glados.cloud/console/checkin'
    origin = "https://glados.cloud"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    payload={
        'token': 'glados.cloud'
    }
    i=0
    while i <= len(cookies)-1:
        cookie=cookies[i]
    # for cookie in cookies:
        checkin = requests.post(url,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent,'content-type':'application/json;charset=UTF-8'},data=json.dumps(payload))
        if 'message' in checkin.text:
            msg = checkin.json()['message']
            # 判断域名是否过期
            if msg.find("please checkin via") != -1:
                host=msg[msg.find("https"):]
                url=host+"/api/user/checkin"
                url2=host+"/api/user/status"
                referer=host+"/console/checkin"
                origin=host
                payload['token']=host[8:]
                continue
            i=i+1
            state =  requests.get(url2,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent})
    #--------------------------------------------------------------------------------------------------------#  
            time = state.json()['data']['leftDays']
            if isinstance(time,str):
                time = time.split('.')[0]
            else:
                time=str(time)
                email = state.json()['data']['email']
                points = checkin.json()['list'][0]['balance'].split(".")[0]
                print(email+'----结果--'+msg+'----剩余('+time+')天'+'----点数('+points+')')  # 日志输出
                sendContent += msg+'--剩余('+time+')天'+'--点数('+points+')--'+email+'\n'
        else:
            requests.get('http://www.pushplus.plus/send?token=' + sckey + '&content='+email+'cookie已失效')
            print('cookie已失效')  # 日志输出
            break
     #--------------------------------------------------------------------------------------------------------#   
    if sckey != "":
         requests.get('http://www.pushplus.plus/send?token=' + sckey + '&title='+email+'签到成功'+'&content='+sendContent)


