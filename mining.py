# -*- coding: UTF-8 -*-
from urllib import request
import chardet
from bs4 import BeautifulSoup
from  ip_pool  import proxy_dict




if __name__ == "__main__":
    proxy = proxy_dict
    proxy_support = request.ProxyHandler(proxy)
    opener = request.build_opener(proxy_support)
    opener.addheaders = [('User-Agent',
                          'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
    request.install_opener(opener)
    response = request.Request("https://blog.csdn.net/c406495762/article/details/71158264")
    response=request.urlopen(response)
    html = response.read()
    charset = chardet.detect(html)
    print(charset)
    html = html.decode(charset['encoding'])
    soup_texts = BeautifulSoup(html, 'lxml')
    texts = soup_texts.find_all('div',class_='article_content')
    soup_text = BeautifulSoup(str(texts), 'lxml')
    # 将\xa0无法解码的字符删除
    print(soup_text.div.text.replace('\xa0', ''))
