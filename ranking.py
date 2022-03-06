import os.path
import time

import openpyxl
import pandas
import sqlite3

workbook = openpyxl.load_workbook('save.xlsx')

now = time.time()
for sheet in workbook.sheetnames:
    dataframe = pandas.read_excel('save.xlsx', sheet_name=sheet, index_col=0)
    print(sheet)
    # dataframe.to_sql(sheet, connector, if_exists='replace')
    # print(dataframe)
print(time.time() - now)
print('\n\n\n')

now = time.time()
for page in workbook.sheetnames:
    connector = sqlite3.connect('save.sqlite')
    dataframe = pandas.read_sql("SELECT * FROM '{}'".format(page), connector)
    connector.close()
    print(page)
    # print(dataframe)

print(time.time() - now)

