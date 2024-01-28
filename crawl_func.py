# -*- coding: utf-8 -*-
"""
Created on 2018/5/18 

@author: susmote
"""

from bs4 import BeautifulSoup

stu_info = {
    'id': '',
    'name': '',
    'department': '',
    'major': '',
    'class': ''
}


def get_student_info(user_table):

    soup = BeautifulSoup(user_table, 'lxml')

    stu_info_keys_list = list(stu_info.keys())
    # 获取学生基本信息
    for i in range(5, 10):
        user_content = soup.find('span', attrs={'id': "Label"+str(i)})
        if i == 9:
            stu_info[(stu_info_keys_list[i - 5])] = user_content.text[4:]
        else:
            stu_info[(stu_info_keys_list[i-5])] = user_content.text[3:]

    return stu_info


def get_timetable_dic(user_table):
    soup = BeautifulSoup(user_table, "html5lib")
    trs = soup.find(id="Table1").find_all('tr')
    classes = []
    for tr in trs:
        tds = tr.find_all('td')
        for td in tds:
            if td.string == None:
                oneClassKeys = ["name", "time", "teacher", "location"]
                oneClassValues = []
                for child in td.children:
                    if child.string != None:
                        oneClassValues.append(child.string)
                while len(oneClassValues) < len(oneClassKeys):
                    oneClassValues.append("")
                oneClass = dict((key, value) for key, value in zip(oneClassKeys, oneClassValues))
                oneClass["timeInTheWeek"] = oneClass["time"].split("{")[0][:2]
                oneClass["timeInTheDay"] = oneClass["time"].split("{")[0][2:]
                oneClass["timeInTheTerm"] = oneClass["time"].split("{")[1][:-1]
                classes.append(oneClass)
    return {"classes": classes}


def timetable_to_html(user_table):
    soup = BeautifulSoup(user_table, 'lxml')
    timetable = soup.find("table", attrs={'id': "Table1"})
    web_content = '''
    <html>
    <head>
    <meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <title>%s的课表</title>
    </head>
    <body>
    %s
    </body>
    </html>
    ''' % (stu_info['name'],str(user_table))
    with open("timetable.html", 'w', encoding="utf8") as timetable:
        timetable.write(web_content)
        timetable.close()


def get_Grade(user_grade):
    soup = BeautifulSoup(user_grade, "html5lib")
    trs = soup.find(id="Datagrid1").findAll("tr")[1:]
    Grades = []
    for tr in trs:
        tds = tr.findAll("td")
        tds = tds[:2] + tds[3:5] + tds[6:9]
        oneGradeKeys = ["year", "term", "name", "type", "credit", "gradePonit", "grade"]
        oneGradeValues = []
        for td in tds:
            oneGradeValues.append(td.string)
        oneGrade = dict((key, value) for key, value in zip(oneGradeKeys, oneGradeValues))
        Grades.append(oneGrade)
    return Grades

