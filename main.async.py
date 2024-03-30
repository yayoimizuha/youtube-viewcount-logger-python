import json
from time import time
from typing import NamedTuple
from aiohttp import ClientSession
from asyncio import gather, run
from os import getenv, getcwd, makedirs
from os.path import join
from urllib.parse import urlencode
from const import playlists, pack_comma
from sqlite3 import connect
from pandas import read_sql, DataFrame, Int64Dtype, NA
from datetime import date

from gemini_title_cleaner import trim_title_with_ai

YTV3_ENDPOINT = 'https://www.googleapis.com/youtube/v3'

YTV3_API_KEY = getenv('YTV3_API_KEY', default='')
if YTV3_API_KEY == '':
    print('No YouTube Data v3 API Key.')
    exit(-1)

SQLITE_DATABASE = join(getcwd(), 'save.sqlite')

TODAY_DATE = date.today().__str__()

makedirs('tsvs', exist_ok=True)


def query_builder(resource_type: str,
                  arg: dict,
                  key: str = YTV3_API_KEY) -> str:
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


async def get_video_data(video_key: str, artist_name: str, session: ClientSession, gemini_cache: dict) -> VideoInfo:
    query = {'arg': {'part': 'statistics,snippet',
                     'fields': 'items(snippet/title,statistics/viewCount)',
                     'id': video_key
                     }, 'resource_type': 'videos'}
    resp = await (await session.get(query_builder(**query))).json()
    # print(resp)
    url = f'https://youtu.be/{video_key}'
    try:
        title = await trim_title_with_ai(resp['items'][0]['snippet']['title'], gemini_cache)
        view_count = int(resp['items'][0]['statistics']['viewCount'])
        return VideoInfo(isError=False, artist_name=artist_name, viewCount=view_count, title=title, url=url)
    except BaseException as exception:
        print(exception)
        return VideoInfo(isError=True, artist_name=artist_name, viewCount=0, title='', url=url)


async def runner() -> None:
    tables: dict[str, DataFrame]
    playlist_index_time = time()
    video_dict = dict()
    sess = ClientSession(trust_env=True)
    await gather(*[list_playlist(playlist.playlist_key, playlist.db_key, sess, video_dict) for playlist in playlists()],
                 return_exceptions=True)
    print(f"YouTube playlists index time: {time() - playlist_index_time:2.3f}s")

    sql_index_time = time()
    connector = connect(SQLITE_DATABASE)
    cursor = connector.cursor()
    table_name = [name[0] for name in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
    cursor.close()
    tables = {name: read_sql(f"SELECT * FROM {pack_comma(name)}", connector, index_col='index') for name in table_name}
    for key, table in tables.items():
        tables[key] = table.reindex(columns=['タイトル'] + sorted(table.columns.tolist()[1:]))
        if key not in video_dict.keys():
            video_dict[key] = set()
        video_dict[key] |= {i.removeprefix('https://youtu.be/') for i in table.index}
    print(f"SQL index time: {time() - sql_index_time:2.3f}s")

    video_info_and_dataframe_settings_time = time()

    with open(join(getcwd(), "gemini-cache.json"), mode="r", encoding="utf-8") as gemini_cache_file:
        gemini_cache = json.loads(gemini_cache_file.read())
    await_video_data = gather(
        *[get_video_data(item, key, sess, gemini_cache) for key, items in video_dict.items() for item in items])

    for dataframe_key in tables.keys():
        column_list = tables[dataframe_key].columns.tolist()[1:]
        tables[dataframe_key][column_list] = tables[dataframe_key][column_list].astype(Int64Dtype()).replace(0, NA)
        tables[dataframe_key].dropna(axis=1, how='all', inplace=True)
        # Today column setting
        tables[dataframe_key][TODAY_DATE] = NA
        tables[dataframe_key][TODAY_DATE] = tables[dataframe_key][TODAY_DATE].astype(Int64Dtype())

    # noinspection PyTypeChecker
    video_data: tuple[VideoInfo] = await await_video_data
    with open(join(getcwd(), "gemini-cache.json"), mode="w", encoding="utf-8") as gemini_cache_file:
        gemini_cache_file.write(json.dumps(gemini_cache, indent=2, ensure_ascii=False))

    print(f"Video info and DataFrame settings time: {time() - video_info_and_dataframe_settings_time:2.3f}s")
    for video in video_data:
        if not video.isError:
            if video.artist_name not in tables.keys():
                tables[video.artist_name] = DataFrame(data={'タイトル': video.title, TODAY_DATE: video.viewCount},
                                                      columns=['タイトル', TODAY_DATE],
                                                      index=[video.url])
                tables[video.artist_name]['タイトル'] = tables[video.artist_name]['タイトル'].astype(str)
                tables[video.artist_name][TODAY_DATE] = tables[video.artist_name][TODAY_DATE].astype(Int64Dtype())
            print(video.url, video.viewCount, '回', sep=' ')
            tables[video.artist_name].at[video.url, TODAY_DATE] = int(video.viewCount)
            tables[video.artist_name].at[video.url, 'タイトル'] = video.title

    await sess.close()

    for key, value in tables.items():
        value.loc[value['タイトル'] == '0', 'タイトル'] = None
        # value['タイトル'].replace('0', None, inplace=True)
        value.to_sql(key, connector, if_exists='replace')
        value.to_csv(join(getcwd(), 'tsvs', key + '.tsv'), sep='\t')

    connector.close()


run(runner())

with open(join(getcwd(), 'tsvs', 'group_list.tsv'), mode='w', encoding='utf8') as f:
    f.writelines('\n'.join({playlist.db_key for playlist in playlists()}))
