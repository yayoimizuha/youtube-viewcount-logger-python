import datetime
from os import getcwd
from os.path import join
from instaloader import Instaloader, Profile
from sqlite3 import connect

loader = Instaloader(sleep=True)
pack_comma = lambda x: f'"{x}"'
conn = connect(database=join(getcwd(), 'instagram.sqlite3'))
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS profile(username TEXT NOT NULL,display_name TEXT,profile_pic_url TEXT);')
cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS username_idx ON profile(username);')
TODAY = datetime.date.today()
print(TODAY)

with open(file="instagram_user.list", mode="r") as f:
    for account in f:
        if account.startswith('#'):
            continue
        account = account.strip()
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {pack_comma(account)}(date TEXT,follower_count INTEGER);')
        cursor.execute(f'CREATE UNIQUE INDEX IF NOT EXISTS date_idx ON {pack_comma(account)}(date);')
        profile = Profile.from_username(loader.context, username=account)
        print(profile.username, profile.full_name, profile.followers, profile.profile_pic_url)

        cursor.execute(f'INSERT OR IGNORE INTO {pack_comma(account)} VALUES (?,?)',
                       (TODAY.__str__(), profile.followers))
        cursor.execute('INSERT INTO profile VALUES (?,?,?)', (account, profile.full_name, profile.profile_pic_url))
        conn.commit()
        break

cursor.close()
conn.close()
