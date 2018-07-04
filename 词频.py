import re
import pymongo
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
from discipline import test#  专业集合
import jieba

client = pymongo.MongoClient('localhost',27017)
ganji = client['datamining']
info = ganji['csdn2']
data = DataFrame(list(info.find()))
# data_new = data.T.drop(['_id','keyword','link'])
data_new = data.T.drop(['_id','author','title','date','简介','链接','clickTimes'])
data_new = np.mat(data_new)
data_new  = np.transpose(data_new )
print(data_new.shape)
print(len(data_new))
word=[]
for i in range(len(data_new)):
    data_new[i, 1] = re.sub("[A-Za-z0-9\!\%\[\]\,\。\'\\n\(\)\\r\=\"\”\“\@\#\$\^\&\*\_\+\-\~\`]", "", str(data_new[i,1]))
    # print(data_new[i,1])
    w = jieba.cut(data_new[i,1])
    for j in w:
        word.append(j)
word = np.mat(word)
word = np.transpose(word)
print(word.shape)#1573747
print(type(word))#numpy.matrixlib.defmatrix.matrix

a = test
click=[]
id=[]
for j in a:
    nu=0
    j = re.sub("[A-Za-z0-9\!\%\[\]\,\。\']", "", str(j))
    h = jieba.cut(j)#关键词分词#,cut_all=True
    for m in h:
        for w in range(len(word)):
            if word[w]==m:
                nu=nu+1
    print(nu)
    id.append(j)
    click.append(nu)


result_output = pd.DataFrame(data={"id": id, "click": click})
result_output.to_csv("csdn2.csv", index=False, quoting=3, encoding='utf-8-sig')

