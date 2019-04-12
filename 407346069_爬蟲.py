# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 12:05:09 2019

@author: Javen
"""
'''
print(soup.select("img[class='itemcov']"))
print(type(soup.select("img[class='itemcov']"))) #list
print((soup.select("img[class='itemcov']")[0])) #第1個<img></img>
print((soup.select("img[class='itemcov']")[1])) #第2個<img></img>
print()
print((soup.select("img[class='itemcov']")[0]['alt'])) #第1個<img></img>'s alt=....
print((soup.select("img[class='itemcov']")[0]['data-original'])) #第1個<img></img>'s data-original=...

print(soup.select("span[class='price']"))
print(type(soup.select("span[class='price']"))) #list
print((soup.select("span[class='price']")[0])) #第1個<span></span>
print()
#List all span[class='price']'s value
for price in soup.select("span[class='price']"): 
    print(price.select('b'))
'''
#引入網頁
import requests
res=requests.get("http://search.books.com.tw/search/query/key/python/call/all")
#print(res.text)

from bs4 import BeautifulSoup
soup=BeautifulSoup(res.text,'html.parser')
#print(soup.title.string)

import pandas as pd

#書名
books=pd.Series()
for book in soup.select("img[class='itemcov']"):
    books=books.append(pd.Series([book['alt']])).reset_index(drop=True)
    
#取價格
i=0
prices=pd.Series()
for price in soup.select("span[class='price']"):
    if(i<books.size):
        if(len(price.select('b'))==1):
            prices=prices.append(pd.Series(price.select('b')[0].string)).reset_index(drop=True)
        elif(len(price.select('b'))==2):
            prices=prices.append(pd.Series(price.select('b')[1].string)).reset_index(drop=True)
        else:
            break;
    i+=1    
    
##取作者
authors=list()
for author in soup.select("li[class='item']"):
    au = author.text.split(",")[1].split("&nbsp")[0].replace("\t" , " ").replace("\n" , " ").strip().split("\xa0")[0]
    authors.append(au)
authors_s = pd.Series( (v for v in authors) )

#取日期
dates= list()
for date in soup.select("li[class='item']"):
    d = date.text.split(":")[1].split("\n")[0].strip()
    dates.append(d) 
dates_s = pd.Series( (v for v in dates) )

df=pd.DataFrame({'價格':prices,'書名':books,'作者':authors_s , '日期':dates_s})    
print(df)
print("資料筆數:",prices.size)