"""
kakao_msg.py 

에러발생시 OPEN API를 사용하여 작동하는 이벤트
OPEN API를 사용하기 위한 필수 요소를 작성한 함수

"""

from tkinter.constants import NONE
import requests
import json
from datetime import *
import time
import Get_data

class kakao_send():
    def tokens():                                                                       #KAKAO메세지를위한 토큰 재발급이 되지않았을때 토큰값을 발급해야함
        url = "https://kauth.kakao.com/oauth/token"         

        data = {                                                                        #메세지를 보내기 위한 필요한 데이터
            "grant_type" : "authorization_code",
            "client_id" : "54b47e65cfb31a7d58a46e6cd9fb1afb",
            "redirect_uri" : "https://localhost.com",
            "code"         : "wK1q2P1Th_gn-omzLEAjYuYkUvL23-Yd5ogrfOZIZhuna3-yOZNp2qhk4l-SMYZK8PE8UAopcFAAAAF8RJHEYQ"
            }                                                                            #정해진 시간안에 리프레쉬 하지않으면 코드 기능 상실                                                                                                            
        response = requests.post(url, data=data)
        tokens = response.json()

        print(tokens)

        with open("kakao_token.json", "w") as fp:
            json.dump(tokens, fp)

    def refreshToken():                                                                   #토큰값 재발급
        with open("kakao_token.json","r") as fp:
            token = json.load(fp)
        REST_API_KEY = "54b47e65cfb31a7d58a46e6cd9fb1afb"
        url = "https://kauth.kakao.com/oauth/token"

        data = {
            "grant_type": "refresh_token",   
            "client_id":f"{REST_API_KEY}",
            "refresh_token": token['refresh_token']                                       #refresh_token 값
        }    
        resp = requests.post(url , data=data)
        token['access_token'] = resp.json()['access_token']
        with open("kakao_token.json", "w") as fp:
            json.dump(token, fp)
        return(token)

    def kakao_text():                                                                      #카카오톡메세지를 보내는 코드
        list_time = []
        list_time.insert(0,time.strftime('%y-%m-%d %H:%M:%S'))
        get_error_code = Get_data.PLC_C()
        error_code = get_error_code.error_code()
        with open("kakao_token.json","r") as fp:    
            tokens = json.load(fp)
        kcreds = {"access_token" : tokens.get('access_token')}
        kheaders = {"Authorization": "Bearer " + kcreds.get('access_token')}
        kakaotalk_template_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"                                        
        naver_url = "https://naver.com"                                                  #web_url 항목을 넣기 위한 주소(아무거나 상관 없음) 필수 조건
        text = f"""{list_time[0]} \nError Code\nEC_Error {error_code[0]}\nMC_Error {error_code[1]}\n에러가 발생했습니다. 기동을 중지합니다."""
        template = {                                                                     #메세지를 구성하는 템플릿 구성
        "object_type": "text",
        "text": text,
        "link":{"web_url" : naver_url}
        }                                                                                                                                                                          
        payload = {"template_object" : json.dumps(template)}                             # JSON 형식 -> 문자열 변환      
        res = requests.post(kakaotalk_template_url, data=payload, headers=kheaders)      # 카카오톡 보내기

        # if res.json().get('result_code') == 0:
        #     # print('메시지를 성공적보냈습니다.')
        # else:
        #     # print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(res.json()))