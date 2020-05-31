import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy
import time
import datetime


keywords = numpy.loadtxt("keywords.txt", delimiter=',',dtype='str')
now = datetime.datetime.now()
list2 = pd.DataFrame({'날짜' : [now.strftime('%m월 %d일')]})
index = 0

for a in keywords:
    
    source = requests.get("http://n-keyword.com/?keyword="+a).text
    soup = BeautifulSoup(source, "html.parser")
    
    hotKeys = soup.select("p.pcCount")
    hotKeys2 = soup.select("p.mobileCount")

    print(a +": "+hotKeys[1].text + " / " +  hotKeys2[1].text)
    if(hotKeys[1].text != "" and hotKeys2[1].text == ""):
        list2[a+("PC")]= int(hotKeys[1].text.replace(',', ''))
        list2[a+("M")]= 0
        list2[a+("Sum")] = int(hotKeys[1].text.replace(',', ''))
    elif (hotKeys[1].text == "" and hotKeys2[1].text != ""):
        list2[a+("PC")]= 0
        list2[a+("M")]=int(hotKeys2[1].text.replace(',', ''))
        list2[a+("Sum")] = int(hotKeys2[1].text.replace(',', ''))
    elif(hotKeys[1].text == "" and hotKeys2[1].text == ""):
        list2[a+("PC")]=0
        list2[a+("M")]=0
        list2[a+("Sum")] =0
    else:
        list2[a+("PC")]= int(hotKeys[1].text.replace(',', ''))
        list2[a+("M")]=int(hotKeys2[1].text.replace(',', ''))
        list2[a+("Sum")] = int(hotKeys[1].text.replace(',', '')) + int(hotKeys2[1].text.replace(',', ''))

    list2[a+(" ")]=""

    #list2.loc[index] = [a , hotKeys[1].text , hotKeys2[1].text]
    index += 1
    
    time.sleep(1)

print(list2)
list2.to_csv('result.csv',encoding="euc-kr")

print("총 [" ,index,"]개의 키워드 출력 완료 되었습니다. result.csv로 저장 완료하였습니다.")

a = input()