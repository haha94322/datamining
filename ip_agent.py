# -*- coding: UTF-8 -*-
from urllib import request
from  ip_pool  import proxy_dict
if __name__ == "__main__":
    #访问网址
    url = 'http://news.baidu.com/'
    #这是代理IP
    proxy = proxy_dict
    #创建ProxyHandler
    proxy_support = request.ProxyHandler(proxy)
    #创建Opener
    opener = request.build_opener(proxy_support)
    #添加User Angent
    opener.addheaders = [('User-Agent','User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
    #安装OPener
    request.install_opener(opener)
    #使用自己安装好的Opener

    try:
        response = request.urlopen(url)
    except:
        print("异常")
    #读取相应信息并解码
    html = response.read().decode("utf-8")
    #打印信息
    print(html)