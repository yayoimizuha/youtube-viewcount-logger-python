from time import time
from typing import Any, NamedTuple
from aiohttp import ClientSession
from asyncio import gather, run, Semaphore
from os import getenv, getcwd, path
from urllib.parse import urlencode
from const import playlists, trim_title
from pprint import pprint
from sqlite3 import connect
from pandas import read_sql, DataFrame, NA,Int64Dtype
from datetime import datetime
from numpy import NaN

YTV3_ENDPOINT = "https://www.googleapis.com/youtube/v3"

API_KEY = getenv('YTV3_API_KEY', default='')
if API_KEY == '':
    print('No API Key.')
    exit(-1)

SQLITE_DATABASE = path.join(getcwd(), "save.sqlite")

TODAY_DATE = datetime.today().date()


def query_builder(resource_type: str,
                  arg: dict,
                  key: str = API_KEY) -> str:
    arg["key"] = key
    base_url: str = "/".join([YTV3_ENDPOINT, resource_type])
    return f"{base_url}?{urlencode(arg)}"


class PlaylistItem(NamedTuple):
    artist_name: str
    item_key: set


class VideoInfo(NamedTuple):
    isError: bool
    title: str
    viewCount: int
    artist_name: str
    url: str


async def list_playlist(playlist_key: str, artist_name: str, session: ClientSession) -> PlaylistItem:
    playlist_item = set()
    next_page_token = str()
    while True:
        query = {'arg': {'part': 'snippet',
                         'fields': 'items/snippet/resourceId/videoId,nextPageToken',
                         'playlistId': playlist_key,
                         'maxResults': 50,
                         'pageToken': next_page_token
                         }, 'resource_type': 'playlistItems'}
        resp = await (await session.get(query_builder(**query))).json()

        playlist_item.update([item['snippet']['resourceId']['videoId'] for item in resp['items']])
        if 'nextPageToken' not in resp:
            break
        else:
            next_page_token = resp['nextPageToken']
    return PlaylistItem(artist_name=artist_name, item_key=playlist_item)


async def get_video_data(video_key: str, artist_name: str, session: ClientSession) -> VideoInfo:
    query = {'arg': {'part': 'statistics,snippet',
                     'fields': 'items(snippet/title,statistics/viewCount)',
                     'id': video_key
                     }, 'resource_type': 'videos'}
    resp = await (await session.get(query_builder(**query))).json()
    # print(resp)
    url = f'https://youtu.be/{video_key}'
    try:
        title = trim_title(resp['items'][0]['snippet']['title'], artist_name=artist_name)
        view_count = int(resp['items'][0]['statistics']['viewCount'])
        return VideoInfo(isError=False, artist_name=artist_name, viewCount=view_count, title=title, url=url)
    except BaseException as exception:
        print(exception)
        return VideoInfo(isError=True, artist_name=artist_name, viewCount=0, title='', url=url)


def pack_comma(txt: str) -> str:
    return '"' + txt + '"'


async def runner() -> None:
    start_time = time()
    connector = connect(SQLITE_DATABASE)
    cursor = connector.cursor()
    table_name = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    table_name = [name[0] for name in table_name]
    print(table_name)
    # exit()
    sess = ClientSession(trust_env=True)
    sem = Semaphore(value=300)
    video_list = await gather(
        *[list_playlist(yt_key, artist_name, sess) for yt_key, artist_name, _ in playlists()],
        return_exceptions=True)
    pprint(video_list)
    for item in video_list:
        if item.artist_name in table_name:
            table_data = read_sql(f"SELECT * FROM {pack_comma(item.artist_name)}", connector, index_col='index')
        else:
            table_data = DataFrame(dtype=Int64Dtype)
        print(item.artist_name)
        view_counts = await gather(*[get_video_data(key, item.artist_name, sess) for key in item.item_key])
        pprint(view_counts)
        # print("aaa")
        # print(table_data)
        print(table_data)
        for view_count in view_counts:
            if not view_count.isError:
                print(view_count.title)
                table_data.at[view_count.url, TODAY_DATE] = int(view_count.viewCount)
                table_data.at[view_count.url, 'タイトル'] = view_count.title
            else:
                table_data.at[view_count.url, TODAY_DATE] = 0
        print(table_data)
        print("aa")
        await sess.close()
        exit()
    print(time() - start_time)
    await sess.close()


run(runner())
