# -*- coding: utf-8 -*-
"""
Created on 2018/5/18 

@author: susmote
"""
from bs4 import BeautifulSoup


def get_operate_link(host, url_content):

    soup=BeautifulSoup(url_content,'lxml')
    user_link = soup.findAll('a', attrs={'target':'zhuti'})
    print(type(user_link))
    operate_link = {}
    for link in user_link:
        operate_link[link.text] = 'http://'+host + "/" + link['href']

    return operate_link