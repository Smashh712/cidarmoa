import hashlib
import hmac
import base64
import json
import time
import random
import requests
import datetime
import pandas as pd
import numpy
import datetime
import time

class Signature:

    @staticmethod
    def generate(timestamp, method, uri, secret_key):
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)

        hash.hexdigest()
        return base64.b64encode(hash.digest())

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}


BASE_URL = 'https://api.naver.com'
API_KEY = '0100000000af8f3b46fc2b15957f6c8a0a73551e641a42ca2baaabf99c7b6cb228635b3ad6'
SECRET_KEY = 'AQAAAACvjztG/CsVlX9sigpzVR5ko/sVIL14o6t/Y5qZcjGGVQ=='
CUSTOMER_ID = '1943092'
uri = '/keywordstool'
method = 'GET'

now = datetime.datetime.now()
keywords = list(numpy.loadtxt("keywords.txt", delimiter=',',dtype='str'))
list2 = pd.DataFrame({'날짜' : [now.strftime('%Y-%m-%d')]})

for number in range(int(len(keywords)/5)+1):
    five_keys = keywords[number*5:(number*5)+5]
    r = requests.get(BASE_URL + uri, params={'hintKeywords':list(five_keys),"howDetail" : 0}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
    for i in five_keys:
        index = 0
        while(1):
            if(r.json()["keywordList"][index]['relKeyword'] == i or  index == 1000):
                print(r.json()["keywordList"][index])
                list2[i+("PC")]= r.json()["keywordList"][index]['relKeyword']
                list2[i+("M")]= r.json()["keywordList"][index]['monthlyPcQcCnt']
                list2[i+("Sum")]= r.json()["keywordList"][index]['monthlyMobileQcCnt']
                list2[i+(" ")]=""
                break
            index+=1
gbgnb 
    time.sleep(1)

print(list2)
list2.to_csv('result.csv',encoding="euc-kr")

print("출력 완료 되었습니다. result.csv로 저장 완료하였습니다.")
a = input()