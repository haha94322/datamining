from bs4 import BeautifulSoup
import subprocess as sp
from lxml import etree
import requests
import random
import re
from urllib import request

page = 1
# requests的Session可以自动保持cookie,不需要自己维护cookie内容
S = requests.Session()

target_url = 'http://www.xicidaili.com/nn/%d' % page
# 完善的headers
opener = {'Upgrade-Insecure-Requests': '1',
                     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                     'Referer': 'http://www.xicidaili.com/nn/',
                     'Accept-Encoding': 'gzip, deflate, sdch',
                     'Accept-Language': 'zh-CN,zh;q=0.8',
                     }
# get请求
target_response = S.get(url=target_url, headers=opener)
# utf-8编码
target_response.encoding = 'utf-8'
# 获取网页信息
target_html = target_response.text
# 获取id为ip_list的table
bf1_ip_list = BeautifulSoup(target_html, 'lxml')
bf2_ip_list = BeautifulSoup(str(bf1_ip_list.find_all(id='ip_list')), 'lxml')
ip_list_info = bf2_ip_list.table.contents
# 存储代理的列表
proxys_list = []
# 爬取每个代理信息
for index in range(len(ip_list_info)):
    if index % 2 == 1 and index != 1:
        dom = etree.HTML(str(ip_list_info[index]))
        ip = dom.xpath('//td[2]')
        port = dom.xpath('//td[3]')
        protocol = dom.xpath('//td[6]')
        proxys_list.append(protocol[0].text.lower() + '#' + ip[0].text + '#' + port[0].text)