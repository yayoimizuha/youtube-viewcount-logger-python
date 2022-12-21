from time import time
from typing import Any
from aiohttp import ClientSession
from asyncio import gather, run
from os import getenv, EX_CONFIG
from urllib.parse import urlencode
from const import playlists
from pprint import pprint

YTV3_ENDPOINT = "https://www.googleapis.com/youtube/v3"

API_KEY = getenv('YTV3_API_KEY', default='')
if API_KEY == '':
    print('No API Key.')
    exit(EX_CONFIG)


def query_builder(resource_type: str,
                  arg: dict,
                  key: str = API_KEY) -> str:
    arg["key"] = key
    base_url: str = "/".join([YTV3_ENDPOINT, resource_type])
    return f"{base_url}?{urlencode(arg)}"


async def list_playlist(yt_key: str, artist_name: str, session: ClientSession) -> dict[Any, Any]:
    playlist_item = list()
    next_page_token: str = ''
    while True:
        query = {"arg": {"part": 'snippet',
                         "fields": 'items/snippet/resourceId/videoId,nextPageToken',
                         "playlistId": yt_key,
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


async def runner() -> None:
    start_time: float = time()
    sess = ClientSession(trust_env=True)
    video_list = await gather(
        *[list_playlist(yt_key, artist_name, sess) for yt_key, artist_name, _ in playlists()], return_exceptions=True)
    pprint(video_list)
    await sess.close()
    print(time() - start_time)


run(runner())
