# import pymysql
# import pandas as pd
#
# time_str = "2024-10-21 23:59:59"
#
# conn = pymysql.connect(host="8.138.173.53", user="root", password="cy19991116", database="grade_feedback")
#
# # 创建游标对象，用于执行SQL查询
# cursor = conn.cursor()
# sql = "INSERT INTO grade_feedback.student_info(studentId, password, studentName) VALUES (%s, %s, %s)"
# values = []
# df = pd.read_excel('账号.xlsx')
#
# cols = df.columns
# for index, row in df.iterrows():
#     name = row['姓名']
#     id = row['学号']
#     password = row['密码']
#     values.append((id, password, name))
#
# print(values)
# cursor.executemany(sql, values)
# conn.commit()
# conn.close()
