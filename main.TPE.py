from time import time
from typing import Any
from aiohttp import ClientSession
from asyncio import gather, run, Semaphore
from os import getenv, getcwd, path
from urllib.parse import urlencode
from const import playlists, trim_title
from pprint import pprint
from sqlite3 import connect
from pandas import read_sql, DataFrame
from datetime import datetime

YTV3_ENDPOINT = "https://www.googleapis.com/youtube/v3"

API_KEY = getenv('YTV3_API_KEY', default='')
if API_KEY == '':
    print('No API Key.')
    exit(-1)

SQLITE_DATABASE = path.join(getcwd(), "save.sqlite")

TODAY_DATE = datetime.today()


def query_builder(resource_type: str,
                  arg: dict,
                  key: str = API_KEY) -> str:
    arg["key"] = key
    base_url: str = "/".join([YTV3_ENDPOINT, resource_type])
    return f"{base_url}?{urlencode(arg)}"


async def list_playlist(playlist_key: str, artist_name: str, session: ClientSession) -> dict[Any, Any]:
    playlist_item = list()
    next_page_token = str()
    while True:
        query = {"arg": {"part": 'snippet',
                         "fields": 'items/snippet/resourceId/videoId,nextPageToken',
                         "playlistId": playlist_key,
                         "maxResults": 50,
                         "pageToken": next_page_token
                         }, "resource_type": "playlistItems"}
        resp = await (await session.get(query_builder(**query))).json()
        playlist_item.extend(resp['items'])
        if 'nextPageToken' not in resp:
            break
        else:
            next_page_token = resp['nextPageToken']
    return {artist_name: [item['snippet']['resourceId']['videoId'] for item in playlist_item]}


async def get_video_data(video_key: str, artist_name: str, session: ClientSession):
    pass


async def runner() -> None:
    start_time: float = time()
    connector = connect(SQLITE_DATABASE)
    cursor = connector.cursor()
    table_name = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    table_name = [name[0] for name in table_name]
    all_table_data = dict()
    for name in table_name:
        all_table_data[name] = read_sql(f"SELECT * FROM \u0022{name}\u0022", connector, index_col='index')
    print(table_name)
    exit()
    sess = ClientSession(trust_env=True)
    sem = Semaphore(value=300)
    video_list = await gather(
        *[list_playlist(yt_key, artist_name, sess) for yt_key, artist_name, _ in playlists()],
        return_exceptions=True)
    pprint(video_list)
    await sess.close()
    print(time() - start_time)
    for item in video_list:
        name = list(item.keys())[0]
        print(name)
        print(set(item[name]))


run(runner())
