import asyncio
import os
import pprint
import time
from aiogoogle import Aiogoogle, auth
import const


async def google_api():
    async with Aiogoogle(api_key=auth.creds.ApiKey(os.environ["YTV3_API_KEY"])) as aiogoogle:
        youtube_v3 = await aiogoogle.discover(api_name="youtube", api_version="v3")
        all_musics = await asyncio.gather(
            *[youtube_data_api_v3(playlist_key=playlist_key, group=group, build=youtube_v3, aio=aiogoogle) for
              playlist_key, group, _ in const.playlists()])
        pprint.pprint(all_musics)


async def youtube_data_api_v3(playlist_key: str, group: str, build: Aiogoogle.discover, aio: Aiogoogle):
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


start_time = time.time()
asyncio.run(google_api())
print(time.time() - start_time)
