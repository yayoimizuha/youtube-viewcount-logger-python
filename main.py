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
pandas.options.display.colheader_justify = 'left'

API_KEY = os.getenv('API_KEY', default='')

if API_KEY == '':
    print('No API Key.')
    exit(-1)
youtube = build(
    'youtube',
    'v3',
    developerKey=API_KEY
)
playlistKey = 'PLAAEA82D2950BC77D'

channelId = youtube.playlistItems().list(part='snippet',
                                         fields='items/snippet/channelId',
                                         playlistId=playlistKey,
                                         maxResults=1).execute()['items'][0]['snippet']['channelId']
print(channelId)
channelInfo = youtube.channels().list(
    part='snippet,brandingSettings,statistics',
    fields='items(snippet(thumbnails/high,title),'
           'brandingSettings/image,'
           'statistics(subscriberCount,videoCount,viewCount))',
    id=channelId).execute()
pprint(channelInfo)
# exit(0)
nextPageToken = ''
videoId = []
while True:
    playlist = youtube.playlistItems().list(part='snippet',
                                            fields='items/snippet/resourceId/videoId,nextPageToken',
                                            playlistId=playlistKey,
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
current_data = []
for Id in videoId:
    video_info = youtube.videos().list(part='statistics,snippet',
                                       fields='items(snippet(title,thumbnails(high,maxres)),'
                                              'statistics/viewCount)',
                                       id=Id).execute()
    video_info = json.loads(unicodedata.normalize('NFKC', json.dumps(video_info)))['items']
    # print(video_info)
    # pprint(video_info)
    if 'maxres' in video_info[0]['snippet']['thumbnails']:
        thumb = video_info[0]['snippet']['thumbnails']['maxres']
        # print('maxres')
    else:
        thumb = video_info[0]['snippet']['thumbnails']['high']
        # print('high')
    # pprint(video_info[0]["snippet"]["thumbnails"])
    data = [[thumb['url'], thumb['width'], thumb['height']],
            unicodedata.normalize('NFKC', video_info[0]['snippet']['title']),
            video_info[0]['statistics']['viewCount'],
            'https://youtu.be/' + Id]
    # pprint(data)
    current_data.append(data)

pprint(current_data)

today = str(datetime.date.today())
dataframe = pandas.DataFrame([0])
if 'タイトル' not in dataframe.columns:
    dataframe['タイトル'] = ''
if today not in dataframe.columns:
    dataframe[today] = 0

for data in current_data:
    url = str(data[3])
    if data[3] not in dataframe.index.tolist():
        dataframe.loc[url] = 0
    # print(dataframe)
    dataframe.at[url, 'タイトル'] = data[1]
    dataframe.at[url, today] = int(data[2])

dataframe.drop(0, axis=0, inplace=True)
dataframe.drop(0, axis=1, inplace=True)

print(dataframe)
print((datetime.date.today() - datetime.date(2021, 1, 1)).days)

dataframe.to_excel('text.xlsx', sheet_name=channelInfo['items'][0]['snippet']['title'])

wb = openpyxl.Workbook()
