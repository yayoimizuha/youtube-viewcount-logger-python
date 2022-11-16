import asyncio
import os
import pprint
import sys
import time
from aiogoogle import Aiogoogle, auth, GoogleAPI
from const import playlists
import trim_title


async def list_playlist():
    async with Aiogoogle(api_key=auth.creds.ApiKey(os.environ["YTV3_API_KEY"])) as aiogoogle:
        youtube_v3: GoogleAPI = await aiogoogle.discover(api_name="youtube", api_version="v3")
        all_videos = await asyncio.gather(
            *[list_playlist_content(playlist_key=playlist_key, group=group, build=youtube_v3, aio=aiogoogle)
              for playlist_key, group, _ in playlists()], return_exceptions=True)
        return all_videos


async def list_playlist_content(playlist_key: str, group: str, build: Aiogoogle.discover, aio: Aiogoogle) -> \
        list[str, list[str]]:
    res = await aio.as_api_key(build.playlistItems.list(part='snippet',
                                                        fields='items/snippet/resourceId/videoId,nextPageToken',
                                                        playlistId=playlist_key,
                                                        maxResults=50
                                                        ))
    video_list: list[str] = [key["snippet"]["resourceId"]["videoId"] for key in res["items"]]
    while res.get('nextPageToken', False):
        res = await aio.as_api_key(build.playlistItems.list(part='snippet',
                                                            fields='items/snippet/resourceId/videoId,nextPageToken',
                                                            playlistId=playlist_key,
                                                            maxResults=50,
                                                            pageToken=res["nextPageToken"]
                                                            ))
        video_list.extend([key["snippet"]["resourceId"]["videoId"] for key in res["items"]])
    return [group, video_list]


async def view_count_getter(key: tuple[str, str], build: Aiogoogle.discover, aio: Aiogoogle) -> list[list[str], dict]:
    print("start", key, time.time() - start_time)
    res = await aio.as_api_key(build.videos.list(
        part='statistics,snippet',
        fields='items(snippet/title,statistics/viewCount)',
        id=key[1]
    ))
    print("end", key, time.time() - start_time)
    return [key, *res["items"]]


async def view_counts(keys: list[tuple[str, str]]):
    async with Aiogoogle(api_key=auth.creds.ApiKey(os.environ["YTV3_API_KEY"])) as aiogoogle:
        youtube_v3: GoogleAPI = await aiogoogle.discover(api_name="youtube", api_version="v3")
        all_musics = await asyncio.gather(
            *[view_count_getter(key=key, build=youtube_v3, aio=aiogoogle) for key in keys], return_exceptions=True)
        return all_musics


start_time = time.time()
music_video_list = asyncio.run(list_playlist())

# pprint.pprint(music_video_list)

videoId_keys: list[tuple[str, str]] = []
for playlist_list in music_video_list:
    pprint.pprint(playlist_list)
    group_name: str = playlist_list[0]
    videoIds: list = playlist_list[1]
    for videoId in videoIds:
        if not type(videoId) is str:
            print(videoId, file=sys.stderr)
        else:
            videoId_keys.append((group_name, videoId))

view_count_result = asyncio.run(view_counts(videoId_keys))
# pprint.pprint(view_count_result)
for content in view_count_result:
    try:
        group_name: str = content[0][0]
        song_key: str = content[0][1]
        song_name: str = content[1]["snippet"]["title"]
        view_count: int = content[1]["statistics"]["viewCount"]

    except Exception as e:
        print(e, file=sys.__stderr__)
        print()
        continue
    print()
    print(group_name, song_key)
    print(trim_title.trim_title(song_name, group_name), view_count)

print(time.time() - start_time)
