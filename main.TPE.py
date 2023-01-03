from time import time
from typing import NamedTuple
from aiohttp import ClientSession
from asyncio import gather, run
from os import getenv, getcwd, path
from urllib.parse import urlencode
from const import playlists, trim_title
from sqlite3 import connect
from pandas import read_sql, DataFrame, Int64Dtype
from datetime import datetime
from numpy import NaN

YTV3_ENDPOINT = 'https://www.googleapis.com/youtube/v3'

API_KEY = getenv('YTV3_API_KEY', default='')
if API_KEY == '':
    print('No API Key.')
    exit(-1)

SQLITE_DATABASE = path.join(getcwd(), 'save.sqlite')

TODAY_DATE = datetime.today().date().__str__()


def query_builder(resource_type: str,
                  arg: dict,
                  key: str = API_KEY) -> str:
    arg['key'] = key
    base_url: str = '/'.join([YTV3_ENDPOINT, resource_type])
    return f'{base_url}?{urlencode(arg)}'


class VideoInfo(NamedTuple):
    isError: bool
    title: str
    viewCount: int
    artist_name: str
    url: str


async def list_playlist(playlist_key: str, artist_name: str, session: ClientSession, video_dict: dict[str:set[str]]):
    if artist_name not in video_dict:
        video_dict[artist_name] = set()
    next_page_token = str()
    while True:
        query = {'arg': {'part': 'snippet',
                         'fields': 'items/snippet/resourceId/videoId,nextPageToken',
                         'playlistId': playlist_key,
                         'maxResults': 50,
                         'pageToken': next_page_token
                         },
                 'resource_type': 'playlistItems'}
        resp = await (await session.get(query_builder(**query))).json()
        video_dict[artist_name] |= {item['snippet']['resourceId']['videoId'] for item in resp['items']}
        if 'nextPageToken' not in resp:
            break
        else:
            next_page_token = resp['nextPageToken']


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
    return f'\"{txt}\"'


async def runner() -> None:
    tables: dict[str, DataFrame]
    playlist_index_time = time()
    video_dict = dict()
    sess = ClientSession(trust_env=True)
    await gather(*[list_playlist(yt_key, artist_name, sess, video_dict) for yt_key, artist_name, _ in playlists()],
                 return_exceptions=True)
    print(f"YouTube playlists index time: {time() - playlist_index_time:2.3f}s")

    sql_index_time = time()
    connector = connect(SQLITE_DATABASE)
    cursor = connector.cursor()
    table_name = [name[0] for name in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
    tables = {name: read_sql(f"SELECT * FROM {pack_comma(name)}", connector, index_col='index') for name in table_name}
    for key, table in tables.items():
        if key not in video_dict.keys():
            video_dict[key] = set()
        video_dict[key] |= {i.removeprefix('https://youtu.be/') for i in table.index}
    print(f"SQL index time: {time() - sql_index_time:2.3f}s")

    await_video_data = gather(*[get_video_data(item, key, sess) for key, items in video_dict.items() for item in items])

    for dataframe_key in tables.keys():
        tables[dataframe_key][TODAY_DATE] = 0
        column_list = tables[dataframe_key].columns.tolist()[1:]
        for column in column_list:
            tables[dataframe_key].loc[tables[dataframe_key][column] == 0, column] = NaN
            tables[dataframe_key][column] = tables[dataframe_key][column].astype(Int64Dtype())

    # noinspection PyTypeChecker
    video_data: list[VideoInfo] = await await_video_data
    for video in video_data:
        if not video.isError:
            print(video)
            tables[video.artist_name].at[video.url, TODAY_DATE] = int(video.viewCount)

    await sess.close()
    print(tables['鈴木愛理'])


run(runner())
