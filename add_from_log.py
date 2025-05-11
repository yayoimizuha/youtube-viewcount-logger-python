import re
import sqlite3

COLUMN_NAME = "2025-05-11"

with open("scrape.log", mode="r", encoding="utf-8") as fp:
    found = dict(re.findall(r"(https://youtu\.be/[A-z0-9\-_]*)\s(\d*)\s回", fp.read()))

with sqlite3.connect("save.sqlite") as connect:
    cur = connect.cursor()
    for (table_name,) in cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall():
        cur.execute('ALTER TABLE "{}" ADD COLUMN "{}" INTEGER'.format(table_name, COLUMN_NAME))
        for (index,) in cur.execute('SELECT "index" FROM "{}"'.format(table_name)).fetchall():
            if index in found.keys():
                cur.execute('UPDATE "{}" SET "{}" = ? WHERE "index" = ?'.format(table_name, COLUMN_NAME),
                            (found[index], index))
                print((found[index], index))
