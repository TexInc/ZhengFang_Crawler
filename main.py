# -*- coding: utf-8 -*-
"""
Created on 2018/5/18 

@author: susmote
"""

import requests
from bs4 import BeautifulSoup
from PIL import Image
from get_operate_link import get_operate_link
import urllib.parse
from crawl_func import get_timetable_dic,get_student_info,get_Grade

if __name__ == "__main__":

    #全局变量
    host = "127.0.0.1"  # 学校教务管理系统ip地址，可以改成你们学校的

    url='http://'+host + "/" + 'default2.aspx'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Referer': url,
        'Host': host
    }
    session=requests.session()


    # 获取标识码
    soup=BeautifulSoup(session.get(url,headers=headers).text,'lxml')
    __VIEWSTATE=soup.find_all('input',type="hidden")[0]['value']

    # 输入需要的信息 学号，密码，验证码
    studentid = input('输入学号：')
    passwd = input('输入密码：')
    captcha_url = 'http://'+host + "/" + 'CheckCode.aspx'
    r=session.get(captcha_url,headers=headers)
    print(r)
    with open('captcha.jpg','wb') as f:
        f.write(r.content)
    im=Image.open('captcha.jpg')
    im.show()
    im.close()
    checkcode = input("请输入验证码 ： ")

    # 封装需要post的数据
    postdata={
        "__VIEWSTATE": __VIEWSTATE,
        "TextBox1": studentid,
        "TextBox2": passwd,
        "TextBox3": checkcode,
        "Button1": "",
        'RadioButtonList1': '\xd1\xa7\xc9\xfa',
        'Button1': '',
    }

    res = session.post(url, data=postdata, headers=headers)
    if '验证码不正确' in res.text:
        print("你输入的验证码不正确，请重新登录")
        exit()
    elif '密码错误' in res.text:
        print("你输入的学号或密码不正确")
        exit()

    # 登录成功后，返回的是你教务系统的主页源代码
    r = session.get('http://'+host + "/" + 'xs_main.aspx?xh='+ studentid,headers=headers)
    link_dic = get_operate_link(host, r.text)
    for i in range(len(list(link_dic.keys()))):
        print(list(link_dic.keys())[i], ':', link_dic[list(link_dic.keys())[i]])

    # 获取学生个人课表和个人信息
    student_class = session.get(link_dic['学生个人课表'], headers=headers)
    stu_info = get_student_info(student_class.text)
    for i in range(len(list(stu_info.keys()))):
        print(list(stu_info.keys())[i], ':', stu_info[list(stu_info.keys())[i]])
    stu_timetable = get_timetable_dic(student_class.text)
    for i in range(len(stu_timetable['classes'])):
        print(stu_timetable['classes'][i])

    # 查询个人成绩
    student_grade_query = session.get(link_dic['成绩查询'], headers=headers)
    soup = BeautifulSoup(student_grade_query.text, 'lxml')
    __VIEWSTATE = soup.find_all('input', type="hidden")[0]['value']
    query_post_data = {
        '__VIEWSTATE': __VIEWSTATE,
        'ddlXN': '2017-2018',
        'ddlXQ': '1',
        'Button1': '按学期查询'
    }
    query_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Host': host,
        'Referer': urllib.parse.quote(link_dic['成绩查询'], encoding='gbk',safe='/:?=&')
    }
    user_grade = session.post(link_dic['成绩查询'], data=query_post_data, headers=query_header)
    stu_grade = (get_Grade(user_grade.text))
    for i in range(len(stu_grade)):
        print(stu_grade[i])


