import asyncio
import os
import pprint
import time
from aiogoogle import Aiogoogle, auth
import const


async def google_api():
    async with Aiogoogle(api_key=auth.creds.ApiKey(os.environ["YTV3_API_KEY"])) as aiogoogle:
        youtube_v3 = await aiogoogle.discover(api_name="youtube", api_version="v3")
        for playlist_key, group, make_summary in const.playlists():
            print(group)
            res = await aiogoogle.as_api_key(youtube_v3.playlistItems.list(part='snippet',
                                                                           fields='items/snippet/resourceId/videoId,nextPageToken',
                                                                           playlistId=playlist_key,
                                                                           maxResults=50
                                                                           ))
            video_list: list[str] = [key["snippet"]["resourceId"]["videoId"] for key in res["items"]]
            while res.get('nextPageToken', False):
                res = await aiogoogle.as_api_key(youtube_v3.playlistItems.list(part='snippet',
                                                                               fields='items/snippet/resourceId/videoId,nextPageToken',
                                                                               playlistId=playlist_key,
                                                                               maxResults=50,
                                                                               pageToken=res["nextPageToken"]
                                                                               ))
                video_list.extend([key["snippet"]["resourceId"]["videoId"] for key in res["items"]])
            pprint.pprint(video_list)


start_time = time.time()
asyncio.run(google_api())
print(time.time() - start_time)
