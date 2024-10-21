import openpyxl
import csv
import pandas as pd

# open given workbook
# and store in excel object
excel = openpyxl.load_workbook("15.7前测.xlsx")

# select the active sheet
sheet = excel.active

# writer object is created
col = csv.writer(open("15.7前测.csv",
                      'w',
                      newline=""))

# writing the data in csv file
for r in sheet.rows:
    # row by row write
    # operation is perform
    col.writerow([cell.value for cell in r])
