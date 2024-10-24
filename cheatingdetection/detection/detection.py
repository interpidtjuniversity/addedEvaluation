import os
import pandas as pd
from openpyxl import load_workbook

pwd = os.getcwd()
files = os.listdir(pwd)

ans_map = {}
ans = []

for file in files:
    if file.endswith(".xlsx"):
        workbook = load_workbook(filename=file)
        sheet = workbook['Sheet1']
        student_names = [cell.value for cell in sheet['A']][1:]
        student_numbers = [cell.value for cell in sheet['B']][1:]
        cheats = [cell.value for cell in sheet['AY']][1:]

        for idx, number in enumerate(student_numbers):
            if number not in ans_map:
                ans_map[number] = {
                    'name': student_names[idx],
                    'number': number,
                }
            if cheats[idx] == 'Y':
                ans_map[number][file[:5]] = '作弊'
            else:
                ans_map[number][file[:5]] = None

for number, details in ans_map.items():
    ans.append(details)

df_data = {}
df_name = []
df_number = []

for item in ans:
    df_name.append(item['name'])
    df_number.append(item['number'])

df_data['姓名'] = df_name
df_data['学号'] = df_number
for file in files:
    if file.endswith(".xlsx"):
        result = []
        title = file[:5]
        for item in ans:
            if title not in item:
                result.append('未作答')
            else:
                result.append(item[title])
        df_data[title] = result

df = pd.DataFrame(df_data)  # 创建DataFrame
df.to_excel("检测结果.xlsx", index=False)  # 存表，去除原始索引列（0,1,2...）