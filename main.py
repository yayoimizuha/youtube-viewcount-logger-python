import json
import os
import time
import unicodedata
from pandas import DataFrame
from googleapiclient.discovery import build
from pprint import pprint
import tweepy
import datetime
import pandas
import openpyxl

pandas.options.display.max_rows = None
pandas.options.display.max_columns = None
pandas.options.display.width = 6000
pandas.options.display.max_colwidth = 6000

API_KEY = os.getenv('API_KEY', default='')

if API_KEY == '':
    print('No API Key.')
    exit(-1)
youtube = build(
    'youtube',
    'v3',
    developerKey=API_KEY
)

nextPageToken = ''
videoId = []
while True:
    playlist = youtube.playlistItems().list(part='snippet',
                                            fields='items/snippet/resourceId/videoId,nextPageToken',
                                            playlistId='PLs8AlpdTjgwdSDETD55q0i3W98tC9SAur',
                                            maxResults=50,
                                            pageToken=nextPageToken).execute()

    # pprint(playlist['items'])
    for Id in playlist['items']:
        videoId.append(Id['snippet']['resourceId']['videoId'])
    if 'nextPageToken' not in playlist:
        break
    nextPageToken = str(playlist['nextPageToken'])
    # break
    # print('\t' + nextPageToken)
    # time.sleep(3)

# pprint(videoId)
for Id in videoId:
    video_info = youtube.videos().list(part='statistics,snippet',
                                       fields='items(snippet(title,thumbnails(high,maxres)),statistics/viewCount)',
                                       id=Id).execute()
    video_info = json.loads(unicodedata.normalize('NFKC', json.dumps(video_info)))['items']
    # print(video_info)
    # pprint(video_info)
    if 'maxres' in video_info[0]['snippet']['thumbnails']:
        thumb = video_info[0]['snippet']['thumbnails']['maxres']
        print('maxres')
    else:
        thumb = video_info[0]['snippet']['thumbnails']['high']
        print('high')
    # pprint(video_info[0]["snippet"]["thumbnails"])
    data = [[thumb['url'], thumb['width'], thumb['height']],
            unicodedata.normalize('NFKC', video_info[0]['snippet']['title']),
            video_info[0]['statistics']['viewCount'],
            'https://youtu.be/' + Id]
    pprint(data)

print((datetime.date.today() - datetime.date(2022, 1, 1)).days)

wb = openpyxl.Workbook()

