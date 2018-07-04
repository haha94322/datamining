#导入相应的包
import pymongo
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
from discipline import test#  专业集合
import re

#连接数据库
client = pymongo.MongoClient('localhost',27017)
ganji = client['datamining']
info = ganji['csdn']
#加载数据
data = DataFrame(list(info.find()))
#删除不想要的字段
data_new = data.T.drop(['_id','author','title','date','简介','链接'])
data_new = np.mat(data_new)
data_new  = np.transpose(data_new )
# print(data_new)
# print(data_new[1,1])
# int(data_new[0,1])
# print(len(data_new))
a = test
click=[]
id=[]
for j in a:
    nu=0
    j = re.sub("[A-Za-z0-9\!\%\[\]\,\。\']", "", str(j))
    # print(type(j))
    for i in range(len(data_new)):
        aim= re.sub("[A-Za-z0-9\!\%\[\]\,\。\']", "", data_new[i,1])
        # print(type(data_new[i,1]))
        if aim==j:
            nu=int(data_new[i,0])+nu
            print(nu)
    id.append(j)
    click.append(nu)
print(click)

result_output = pd.DataFrame(data={"id": id, "click": click})
result_output.to_csv("lstm11.csv", index=False, quoting=3, encoding='utf-8-sig')