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




html = getHTMLText("http://news.baidu.com/ns?cl=2&rn=20&tn=news&word=新工科%20人工智能")
soup = BeautifulSoup(html, "html.parser")
data = soup.find_all('div' , class_='result')
for dl in data:
    ldt1 = dl.find_all("h3")  # dt里储存着博客的题目
    for dt in ldt1:
        # print (type(dt.get_text()))
        text = dt.get_text()
        title = re.sub("[A-Za-z0-9\!\%\[\]\,\。\'\>\ \\n]", "", str(text))
        print("标题是：" + title)
        link = dt.find("a")
        link = link.get("href")
        print(link)





