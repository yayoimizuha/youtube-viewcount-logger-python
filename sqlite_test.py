import datetime
import os.path
import sqlite3
import time
import pandas

SQLITE_FILE = os.path.join(os.getcwd(), "save.sqlite")


def pack_comma(txt: str) -> str:
    return '"' + txt + '"'


start_time = time.time()
connector = sqlite3.connect(SQLITE_FILE)
cursor = connector.cursor()
for table_name in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall():
    print(*table_name)
    # cursor.execute(f"SELECT * FROM {pack_comma(*table_name)};")
    # cursor.execute(f"SELECT * FROM sqlite_master WHERE name={pack_comma(*table_name)};")
    cursor.execute(f"PRAGMA table_info({pack_comma(*table_name)});")
    # cursor.execute(f"ALTER TABLE {pack_comma(*table_name)} MODIFY * AUTOINCREMENT;")
    date_column = [i[1] for i in cursor.fetchall()[2:]]
    print(date_column)
    dataframe = pandas.read_sql(f"SELECT * FROM {pack_comma(*table_name)}", connector, index_col='index')
    # dataframe.to_excel(str(*table_name) + ".xlsx")
    # print(dataframe)
    # print(cursor.fetchall())
    print({"name": str(*table_name),
           "keys": [str(i).removeprefix("https://youtu.be/") for i in dataframe.index.tolist()]})
print(time.time() - start_time)
cursor.close()
connector.close()

print(datetime.date.today())
