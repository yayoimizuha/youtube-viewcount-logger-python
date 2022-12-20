from googleapiclient.discovery import build
from concurrent.futures import ThreadPoolExecutor, as_completed
from os import getenv, getcwd, path, environ, cpu_count
from const import playlists
from pprint import pprint

API_KEY = getenv('YTV3_API_KEY', default='')

if API_KEY == '':
    print('No API Key.')
    exit(-1)
youtube = build(
    'youtube',
    'v3',
    developerKey=API_KEY
)

print(playlists())


def process_channel(artistName, playlistKey):
    channelInfo = youtube.channels().list(
        part='snippet,brandingSettings,statistics',
        fields='items(snippet/thumbnails/high,'
               'brandingSettings/image,'
               'statistics(subscriberCount,videoCount,viewCount))',
        id=youtube.playlistItems().list(part='snippet',
                                        fields='items/snippet/channelId',
                                        playlistId=playlistKey,
                                        maxResults=1).execute()['items'][0]['snippet']['channelId']).execute()
    pprint(channelInfo)


thread_executor = ThreadPoolExecutor(max_workers=cpu_count())
resp = list()
for key, name, _ in playlists():
    resp.append(thread_executor.submit(process_channel, name, key))

for future in as_completed(resp):
    print(future.result())
