import requests
from urllib import request
from bs4 import BeautifulSoup
import chardet
from  ip_pool  import ip
import random
from discipline import test#  专业集合
import time
import pymongo
import re
import numpy as np

def ip_agent():   #更换代理
    proxy_dict=ip()
    proxy = proxy_dict
    proxy_support = request.ProxyHandler(proxy)
    opener = request.build_opener(proxy_support)
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        # "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        # "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        # "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        # "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        # "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        # "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        # "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        # "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        # "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        # "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        # "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        # "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
    ]
    UA = random.choice(user_agent_list)
    opener.addheaders = [('User-Agent',UA)]
    request.install_opener(opener)


    return proxy_dict

def txt(text):    #获取链接文章
    response = request.Request(text)
    response = request.urlopen(response)
    html = response.read()
    charset = chardet.detect(html)
    html = html.decode(charset['encoding'])
    soup_texts = BeautifulSoup(html, 'lxml')
    text = soup_texts.get_text()

    return text

def wrong(text,i):  #增加鲁棒性
    try:
        b=txt(text)
        return b
    except:
        if i<3:
            time.sleep(4)
            ip_agent()
            i=i+1
            wrong(text,i)  # 183.151.39.214:36528

    else:
        pass


def getHTMLText(url):  # 作用：得到html的text
    try:
        print(url)
        r = requests.get(url, timeout=30)
        r.raise_for_status
        r.encoding = "utf-8"
        return r.text
    except:
        # print ("getHTMLText出现异常")
        return "getHTMLText出现异常"

def getInformation(soup,newsdata,keyword):  # 作用：将html的有用信息筛选出来并储存到相对应的列表alist中

    # 通过查看网页源代码，分析得到下面的解析特点。
    data = soup.find_all('div', class_='result')
    for dl in data:
        ldt1 = dl.find_all("h3")  # dt里储存着博客的题目
        for dt in ldt1:
            # print (type(dt.get_text()))
            text = dt.get_text()
            title = re.sub("[A-Za-z0-9\!\%\[\]\,\。\'\>\ \\n]", "", str(text))
            print("标题是：" + title)
            link = dt.find("a")
            link = link.get("href")
            i = 1
            c = wrong(link, i)





        newsdata.insert_one({'title': title, 'link': link, 'txt': c, 'keyword': keyword})#, 'txt': c




        print("**********************************************************")

def datamining(keyword,newsdata):
    for i in range(2,3):
        i=i*20
        html = getHTMLText(r"http://news.baidu.com/ns?word=" + keyword + "&pn="+ str(i) + "&cl=2&ct=1&tn=news&rn=20&ie=utf-8&bt=0&et=0")
        soup = BeautifulSoup(html, "html.parser")
        getInformation(soup, newsdata, keyword)



def wrong2(keyword, newsdata,i):
    try:
        datamining(keyword, newsdata)
    except:
        if i < 5:
            time.sleep(4)
            ip_agent()
            i = i + 1
            wrong2(keyword, newsdata,i)

    else:
        pass



if __name__ == '__main__':
    time_start = time.time()
    conn = pymongo.MongoClient(host='localhost', port=27017)
    toutiao = conn['datamining']
    # 选择或者创建数据集合
    newsdata = toutiao['baidu3']
    # newsdata.remove({})
    a = test
    for j in a:
            time.sleep(2)
            ip_agent()
            j = re.sub("[A-Za-z0-9\!\%\[\]\,\。\']", "", str(j))
            keyword = j
            print(keyword)
            i = 1
            wrong2(keyword, newsdata, i)

    # for j in a:
    #         time.sleep(2)
    #         ip_agent()
    #         n = n + 1
    #         j = re.sub("[A-Za-z0-9\!\%\[\]\,\。\']", "", str(j))
    #         keyword = j
    #         print(keyword)
    #         i = 1
    #         try:
    #             datamining(keyword, newsdata)
    #         except:
    #             if i < 6:
    #                 time.sleep(4)
    #                 ip_agent()
    #                 n = n + 1
    #                 i = i + 1
    #                 datamining(keyword, newsdata)
    #         else:
    #             pass
    time_end = time.time()
    print(time_end - time_start)  # 954.0552804470062s
                                  # 1087.0125703811646s
    print("s")
    # print(n)
# 999.4650814533234s
# 82
# 1095.8077716827393s
# 82
# 1204.7771973609924s
# 82
# 4042.78875s
