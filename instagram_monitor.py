import asyncio
import datetime
import json
import os
from os import getcwd
from os.path import join
import requests
from bs4 import BeautifulSoup

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


def find_json_id(json_data: dict, target_id: str):
    if isinstance(json_data, dict):
        if target_id in json_data:
            return json_data[target_id]
        else:
            for value in json_data.values():
                result = find_json_id(value, target_id)
                if result:
                    return result
    elif isinstance(json_data, list):
        for item in json_data:
            result = find_json_id(item, target_id)
            if result:
                return result
    return None


with open(file="instagram_user.list", mode="r") as f:
    html = requests.get("https://www.instagram.com/").text
    for sjis_scripts in BeautifulSoup(html, "lxml").find_all("script", {"data-sjs": True}):
        if x_ig_app_id := find_json_id(json.loads(sjis_scripts.string), "X-IG-App-ID"):
            break
    if x_ig_app_id is None:
        print("Cannot get X-IG-App-ID...")
        exit(-1)
    for account in f:
        if account.startswith('#'):
            continue
        account = account.strip()

        cursor.execute(f'CREATE TABLE IF NOT EXISTS {pack_comma(account)}(date TEXT,follower_count INTEGER);')
        cursor.execute(f'CREATE UNIQUE INDEX IF NOT EXISTS date_idx ON {pack_comma(account)}(date);')
        try:
            json_obj = requests.get(f"https://www.instagram.com/api/v1/users/web_profile_info/?username={account}",
                                    headers={"X-IG-App-ID": x_ig_app_id}).json()

            # print(json_obj)
            print(full_name := json_obj["data"]["user"]["full_name"])
            print(followers_count := find_json_id(json_obj, "edge_followed_by")["count"], "フォロワー")
            print(profile_pic_url := find_json_id(json_obj, "profile_pic_url_hd"))
            print(post_counts := find_json_id(json_obj, "edge_owner_to_timeline_media")["count"], "投稿")
            # profile = Profile.from_username(loader.context, username=account)
            # print(profile.username, profile.full_name, profile.followers, profile.profile_pic_url)
        except Exception as e:
            print(account, e)
            continue
        cursor.execute(f'INSERT OR IGNORE INTO {pack_comma(account)} VALUES (?,?)',
                       (TODAY.__str__(), followers_count))
        cursor.execute('REPLACE INTO profile VALUES (?,?,?)', (account, full_name, profile_pic_url))
        conn.commit()

cursor.close()
conn.close()
