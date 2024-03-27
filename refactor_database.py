from typing import Callable, Any
from datetime import datetime, timedelta
from pandas import read_sql, to_datetime, concat, Series, DataFrame
from sqlite3 import connect
from os.path import join
from os import getcwd
from copy import deepcopy

connector = connect(join(getcwd(), 'save.sqlite'))
cursor = connector.cursor()
table_names = cursor.execute('SELECT name FROM sqlite_master WHERE type="table";').fetchall()

sayu_df = []
for table_name in table_names:
    dataframe = read_sql(f'SELECT * FROM "{table_name.__getitem__(0)}"', connector, index_col='index')
    if table_name.__getitem__(0) == '道重さゆみ':
        sayumi_column = dataframe.columns
        sayu_df.append(dataframe)
        print('sayu')
    if table_name.__getitem__(0) == 'Buono!':
        second_column = dataframe.columns

print(sayumi_column.__len__(), second_column.__len__())

for a, b in zip(sayumi_column, second_column):
    if a[:4] == '1970':
        print(datetime.fromisoformat('2021-11-22').date() + timedelta(days=int(a.split('.')[1])), end=' ')
    print(a, b)

new_col = []
for a in sayumi_column:
    if a[:4] == '1970':
        new_col.append(datetime.fromisoformat('2021-11-22').date() + timedelta(days=int(a.split('.')[1])))
    else:
        new_col.append(a)

print(new_col)
print(sayu_df[0])
sayu_df[0].columns = new_col
sayu_df[0].to_sql(name='道重さゆみ', con=connector, if_exists='replace')
cursor.close()
connector.close()
