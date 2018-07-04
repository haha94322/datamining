# 通过关键词爬取csdn博客文章

import requests
from urllib import request
from bs4 import BeautifulSoup
import chardet
from  ip_pool  import ip
import random
from discipline import test#  专业集合
import time
import re


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
    texts = soup_texts.find_all('div', class_='article_content')
    soup_text = BeautifulSoup(str(texts), 'lxml')
    a=soup_text.div.text.replace('\xa0', '')
    return a

def wrong(text,i):  #增加鲁棒性
    try:
        b=txt(text)
        return b
    except:
        if i<6:
            time.sleep(4)
            ip_agent()
            i=i+1
            wrong(text,i)  # 183.151.39.214:36528

    else:
        pass





def getHTMLText(url):  # 作用：得到html的text
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status
        r.encoding = "utf-8"
        return r.text
    except:
        # print ("getHTMLText出现异常")
        return "getHTMLText出现异常"




def getInformation(soup,newsdata,keyword):  # 作用：将html的有用信息筛选出来并储存到相对应的列表alist中

    # 通过查看网页源代码，分析得到下面的解析特点。
    A=0
    data = soup.find_all("dl")  # 每个dl里面储存着一篇csdn博客的信息，1个dl里有1个dt和3个dd
    for dl in data:
        ldt = dl.find_all("dt")  # dt里储存着博客的题目
        for dt in ldt:
            # print (type(dt.get_text()))
            text = dt.get_text()
            # print (text)
            indexOfStart = text.find("\n")
            indexOfEnd = text.find("- CSDN博客")
            # print (indexOfStart)
            # print (indexOfEnd)
            title = text[indexOfStart:indexOfEnd - 3].replace("\n", "")
            print("标题是：" + title)
            # print ("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        ldd = dl.find_all("dd")  # 1个dl里有3个dd，分别是作者日期浏览次数，简介，链接
        # 作者日期浏览次数
        text = ldd[0].get_text()
        indexOfStart = text.find("作者")
        indexOfEnd = text.find("日期")
        author = text[indexOfStart + 3:indexOfEnd - 3]
        print("作者是：" + author)

        indexOfStart = text.find("日期")
        indexOfEnd = text.find("浏览")
        date = text[indexOfStart + 3:indexOfEnd - 3]
        print("日期是：" + date)

        text = ldd[0].get_text()
        indexOfStart = text.find("浏览")
        indexOfEnd = text.find("次")
        clickTimes = text[indexOfStart + 3:indexOfEnd - 1]
        print("浏览次数是：" + clickTimes)

        # 简介
        text = ldd[1].get_text()
        text = text.replace("\n", "")
        print("简介是：" + text)

        # 链接
        link = ldd[2].get_text()
        # print("链接是：" + text)
        print(link)

        #文本
        i=1
        c=wrong(link,i)
        A=A+1
        print(A)

        newsdata.insert_one({'title': title, 'author': author, 'date': date, 'clickTimes': clickTimes,
                             '简介': text, '链接': link, 'text': c, 'keyword': keyword })#, 'text': c




        print("**********************************************************")



import pymongo

def datamining(keyword,newsdata):
    for i in range(1, 3):
        html = getHTMLText(r"https://so.csdn.net/so/search/s.do?p=" + str(i) + "&q=" + keyword + "&t=blog&domain=&o=&s=&u=&l=&f=&rbg=0")
        soup = BeautifulSoup(html, "html.parser")
        getInformation(soup, newsdata, keyword)


if __name__ == '__main__':
    time_start = time.time()
    print(time_start)
    conn = pymongo.MongoClient(host='localhost', port=27017)
    toutiao = conn['datamining']
    # 选择或者创建数据集合
    newsdata = toutiao['csdn3']
    # newsdata.remove({})
    a = test
    # # keyword="进程"
    # keyword = ""
    # for i in range(len(a) - 1):
    #     keyword = keyword + a[i] + "+"
    # keyword = keyword + a[-1]
    # # print (keyword)
    n=1
    for j in a:
        time.sleep(2)
        ip_agent()
        n=n+1
        j = re.sub("[A-Za-z0-9\!\%\[\]\,\。\']", "", str(j))
        keyword = j
        print(keyword)
        i=1
        try:
            datamining(keyword,newsdata)
        except:
            if i < 6:
                time.sleep(4)
                ip_agent()
                n=n+1
                i = i + 1
                datamining(keyword,newsdata)
        else:
            pass
    time_end = time.time()
    print(time_end - time_start)    #1220.2313873767853s
    print("s")                      #82
    print(n)                        #2614.3087384700775s