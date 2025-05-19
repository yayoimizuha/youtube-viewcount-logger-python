import asyncio
import datetime
import os
from os import getcwd
from os.path import join

from instaloader import Instaloader, Profile
from sqlite3 import connect

from selenium.webdriver.common.bidi.network import Network
from selenium.webdriver.firefox import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


async def run():
    return
    loader = Instaloader(sleep=True)
    pack_comma = lambda x: f'"{x}"'
    conn = connect(database=join(getcwd(), 'instagram.sqlite3'))
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS profile(username TEXT NOT NULL,display_name TEXT,profile_pic_url TEXT);')
    cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS username_idx ON profile(username);')
    TODAY = datetime.date.today()
    print(TODAY)

    if os.name == 'nt':
        firefox_path = r"C:\Program Files\Firefox Developer Edition\firefox.exe"
    else:
        firefox_path = "/opt/firefox/firefox"

    options = webdriver.Options()
    options.enable_bidi = True
    # options.add_argument("-headless")
    options.binary_location = firefox_path
    try:
        with Firefox(options=options) as driver:
            bidi:Network = driver.network()
            bidi.add_request_handler()

    except Exception as e:
        print(e)

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


if __name__ == '__main__':
    asyncio.run(run())
