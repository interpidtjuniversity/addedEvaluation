import datetime

import pymysql
import pandas as pd

# 修改这里
time_str = "2024-10-21 23:59:59"
TAG = "TAG"

conn = pymysql.connect(host="8.138.173.53", user="root", password="cy19991116", database="grade_feedback")
cursor = conn.cursor()
sql = "INSERT INTO grade_feedback.feedback_table(studentId, examName, studentName, feedbackStatus, feedbackContent, feedbackImages, deadline, tag) VALUES (%s, %s, %s, \"未反馈\", \"\", \"[]\", %s, %s)"
values = []
df = pd.read_excel('检测结果.xlsx')
cols = df.columns
for index, row in df.iterrows():
    name = row['姓名']
    id = row['学号']
    for exam in cols:
        if '姓名'.__contains__(exam) is False and '学号'.__contains__(exam) is False:
            result = row[exam]
            if isinstance(result, str) and '作弊'.__contains__(result) is True and '未设置学号'.__contains__(id) is False:
                values.append((id, exam, name, datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S'), TAG))

cursor.executemany(sql, values)
conn.commit()
conn.close()


# import datetime
# import pymysql
#
# time_str = "2024-10-21 23:59:59"
#
# conn = pymysql.connect(host="8.138.173.53", user="root", password="cy19991116", database="grade_feedback")
#
# # 创建游标对象，用于执行SQL查询
# cursor = conn.cursor()
# sql = "INSERT INTO grade_feedback.feedback_table(studentId, examName, studentName, feedbackStatus, feedbackContent, feedbackImages, deadline, tag) VALUES (%s, %s, %s, \"未反馈\", \"\", \"[]\", %s, %s)"
# args=('42335073','15.5前测', '杨欣羽', datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S'))
# cursor.execute(sql, args=args)
# conn.commit()
# conn.close()