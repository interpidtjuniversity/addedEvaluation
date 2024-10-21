import pymysql
import pandas as pd

conn = pymysql.connect(host="8.138.173.53", user="root", password="cy19991116", database="grade_feedback")
# 修改这个
TAG = "20241021"

# 创建游标对象，用于执行SQL查询
cursor = conn.cursor()
sql = "select studentId, examName, studentName, feedBackStatus from grade_feedback.feedback_table where tag = %s"
cursor.execute(sql, args=(TAG))
data = cursor.fetchall()
conn.commit()
conn.close()

feedback_data = []
for row in data:
    if '已反馈'.__contains__(row[3]):
        feedback_data.append(row)

df = pd.read_excel('分班名单.xlsx')
student_class_map = {}
for class_ in df.head(0).columns.values:
    for student in df[class_].values:
        student_class_map[str(student).strip()] = class_

df_data = {}
df_data_exam_student_map = {}
def process_class(class_):
    for row in feedback_data:
        if student_class_map[row[2].strip()] == class_:
            if row[1] not in df_data_exam_student_map:
                # 最前面空出一行
                names = ["", row[2]]
                df_data_exam_student_map[row[1]] = names
            else:
                df_data_exam_student_map[row[1]].append(row[2])
    maxL = -1
    for key, value in df_data_exam_student_map.items():
        if len(value) > maxL:
            maxL = len(value)

    for key, value in df_data_exam_student_map.items():
        if len(value) < maxL:
            while len(value) < maxL:
                value.append("")
        # 空出一行
        value.append("")
        df_data[key] = value

for class_ in df.head(0).columns.values:
    process_class(class_)

df = pd.DataFrame(df_data)  # 创建DataFrame
df.to_excel("最终名单.xlsx", index=False)
