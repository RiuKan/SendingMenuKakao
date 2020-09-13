#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json
iteration = True
while iteration == True:
        now = datetime.now()
        session = requests.session()
        data = {"loginType":"basic","userType":"S","recruitDiv":"regular","name":"","bdate":"","mobile":"","userId"
:"아이디","password":"비밀번호"}
        respons = session.post("http://portal.ndhs.or.kr/login",data=data,headers={'User-Agent':'Mozilla/5.0 (Windo
ws NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'})
        respons.raise_for_status()
        response = session.get("http://portal.ndhs.or.kr/studentLifeSupport/carte/list?carteDate=%s"%now.strftime('
%Y%m%d'),headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Ch
rome/84.0.4147.125 Safari/537.36'})
        soup = BeautifulSoup(response.text,'html.parser')
        r = datetime.today().weekday()
        middleSoup =str(soup.select('tbody>tr')[r])
        soup2 = BeautifulSoup(middleSoup,'html.parser')
        soup_1 = BeautifulSoup(str(soup2.select('td')[0]),'html.parser')
        soup_2 = BeautifulSoup(str(soup2.select('td')[1]),'html.parser')
        soup_3 = BeautifulSoup(str(soup2.select('td')[2]),'html.parser')
        text = "     %s\n\n\n아침: %s\n\n점심: %s\n\n저녁: %s"%( soup2.th.get_text(),soup_1.get_text(),soup_2.get_t
ext(),soup_3.get_text())
        talk_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        with open("/home/rk930324/kakao_tokens.json","r") as fp:
                tokens = json.load(fp)
        header = {
        "Authorization": "Bearer {%s}"%tokens["access_token"]}
        post = {
                        "object_type": "text",
                        "text": text,
                        "link": {
                        "web_url": "https://developers.kakao.com",
                        "mobile_web_url": "https://developers.kakao.com"
                        "button_title": "바로 확인"
                }
        data = {"template_object":json.dumps(post)}
        res = requests.post(talk_url, headers=header,data = data)
        if res.json().get('result_code') == 0:
                print('메시지를 성공적으로 보냈습니다.')
                iteration = False
        else:
                refresh_tokens = "%s"%tokens["refresh_token"]
                url = "https://kauth.kakao.com/oauth/token"
                API_token = 'API_token'
                data = {
                        "grant_type" : "refresh_token",
                        "client_id" : API_token,
                        "refresh_token" : refresh_tokens
                        }
                response = requests.post(url, data=data)
                new_accesstoken = response.json()
                tokens["access_token"] = new_accesstoken["access_token"]
                with open("/home/rk930324/kakao_tokens.json","w") as fp:
                        json.dump(tokens,fp)
