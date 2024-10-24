import openpyxl
import csv
import pandas as pd

# open given workbook
# and store in excel object
name = "15.7后测"

excel = openpyxl.load_workbook(name + ".xlsx")

# select the active sheet
sheet = excel.active

# writer object is created
col = csv.writer(open(name + ".csv",
                      'w',
                      newline=""))

# writing the data in csv file
for r in sheet.rows:
    # row by row write
    # operation is perform
    col.writerow([cell.value for cell in r])
