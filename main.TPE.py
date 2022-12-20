from aiohttp import ClientSession
import asyncio
from os import getenv
from urllib.parse import urlencode
from const import playlists

YTV3_ENDPOINT = "https://www.googleapis.com/youtube/v3"

API_KEY = getenv('YTV3_API_KEY', default='')
if API_KEY == '':
    print('No API Key.')
    exit(-1)


def query_builder(resource_type: str,
                  arg: dict,
                  key: str = API_KEY) -> str:
    arg["key"] = key
    base_url: str = "/".join([YTV3_ENDPOINT, resource_type])
    return f"{base_url}?{urlencode(arg)}"


async def playlist_channel():
    async with ClientSession(trust_env=True) as session:
        for yt_key, artist_name, _ in playlists():
            url = query_builder(arg={"part": "snippet",
                                     "fields": 'items/snippet/channelId',
                                     "playlistId": yt_key,
                                     "maxResults": 1
                                     }, resource_type="playlistItems")
            async with session.get(url=url) as sess:
                print(await sess.json())


asyncio.run(playlist_channel())
