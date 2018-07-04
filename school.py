import requests
from urllib import request
from bs4 import BeautifulSoup
import chardet
# from  ip_pool  import ip
import random
from discipline import test#  专业集合
import time
import pymongo
import re
import numpy as np

def getHTMLText(url):  # 作用：得到html的text
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status
        r.encoding = "utf-8"
        return r.text
    except:
        # print ("getHTMLText出现异常")
        return "getHTMLText出现异常"

# time_start = time.time()
# conn = pymongo.MongoClient(host='localhost', port=27017)
# toutiao = conn['datamining']
# # 选择或者创建数据集合
# newsdata = toutiao['school']
# newsdata.remove({})



html = getHTMLText("http://news.baidu.com/ns?word=人工智能&tn=news&from=news&cl=2&rn=20&ct=1")
soup = BeautifulSoup(html,"html.parser")
# print(soup)
data = soup.find_all("span")#专业
for i in data:
    div= i.find_all("li")
    for j in  div:
        li=j.find_all("b")
        for a in li:
            b = j.find_all("a")
            for c in  b:
                text = c.get_text()
                print(text[1,:])


# for i in data:
#     div= i.find_all("li")
#     for j in  div:
#         li=j.find_all("ul")
#         for a in li:
#             text = a.find_all("a")
#             for t in text:
#                 text = t.get_text()
#                 print(text)
# data=soup.find_all("div","yxjsin")#学院
# ldt = data[0].find_all("h3")#学院分类
# data=data[0].find_all("a")#学院名
# print(len(data))
# data = data[0].get_text()
# print(data)
# data= data[0].find_all("a")
# print(data)
