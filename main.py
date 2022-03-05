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
from styleframe import StyleFrame

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
playlistKey = 'PLeUX-FlHsb-tGpXYdlTS8rjjqCLxUB-eh'
artistName = '鈴木愛理'
workbookName = 'save.xlsx'

testint = 0


def get_today_count(video_ids):
    global testint
    return_data = []
    for video_id in video_ids:

        video_info = youtube.videos().list(part='statistics,snippet',
                                           fields='items(snippet(title,thumbnails(high,maxres)),'
                                                  'statistics/viewCount)',
                                           id=video_id).execute()
        video_info = json.loads(unicodedata.normalize('NFKC', json.dumps(video_info)))['items']
        # print(video_info)
        if not video_info:
            continue
        testint += 1
        print(testint, end='\t')
        print(video_info[0]['snippet']['title'])
        if 'maxres' in video_info[0]['snippet']['thumbnails']:
            thumb = video_info[0]['snippet']['thumbnails']['maxres']
            # print('maxres')
        else:
            thumb = video_info[0]['snippet']['thumbnails']['high']
            # print('high')
        # pprint(video_info[0]["snippet"]["thumbnails"])
        return_data.append([[thumb['url'], thumb['width'], thumb['height']],
                            unicodedata.normalize('NFKC', video_info[0]['snippet']['title']),
                            video_info[0]['statistics']['viewCount'],
                            'https://youtu.be/' + video_id])

    return return_data


def get_view_count_and_data(Id):
    global testint
    video_info_raw = youtube.videos().list(part='statistics,snippet',
                                           fields='items(snippet(title,thumbnails(high,maxres)),'
                                                  'statistics/viewCount)',
                                           id=Id).execute()['items']
    video_info = json.loads(unicodedata.normalize('NFKC', json.dumps(video_info_raw)))

    if not video_info:
        return None
    testint += 1
    print(testint, end='\t')
    print(video_info[0]['snippet']['title'])
    if 'maxres' in video_info[0]['snippet']['thumbnails']:
        thumb = video_info[0]['snippet']['thumbnails']['maxres']
        # print('maxres')
    else:
        thumb = video_info[0]['snippet']['thumbnails']['high']

    data = [[thumb['url'], thumb['width'], thumb['height']],
            unicodedata.normalize('NFKC', video_info[0]['snippet']['title']),
            video_info[0]['statistics']['viewCount'],
            'https://youtu.be/' + Id]
    return data


def extract_playlist(playlist_key):
    nextPageToken = ''
    return_videoId = []
    while True:
        playlist = youtube.playlistItems().list(part='snippet',
                                                fields='items/snippet/resourceId/videoId,nextPageToken',
                                                playlistId=playlist_key,
                                                maxResults=50,
                                                pageToken=nextPageToken).execute()

        # pprint(playlist['items'])
        for Id in playlist['items']:
            return_videoId.append(Id['snippet']['resourceId']['videoId'])
        if 'nextPageToken' not in playlist:
            break
        nextPageToken = str(playlist['nextPageToken'])
        # break
        # print('\t' + nextPageToken)
        # time.sleep(3)
    return return_videoId


def save_data(save_dataframe, name):
    today = str(datetime.date.today())
    dataframe = pandas.DataFrame([0])
    if 'タイトル' not in dataframe.columns:
        dataframe['タイトル'] = ''
    if today not in dataframe.columns:
        dataframe[today] = 0

    for data in save_dataframe:
        url = str(data[3])
        if data[3] not in dataframe.index.tolist():
            dataframe.loc[url] = 0
        # print(dataframe)
        dataframe.at[url, 'タイトル'] = data[1]
        dataframe.at[url, today] = int(data[2])

    dataframe.drop(0, axis=0, inplace=True)
    dataframe.drop(0, axis=1, inplace=True)

    # print(dataframe)
    print((datetime.date.today() - datetime.date(2021, 1, 1)).days)

    if not os.path.isfile(workbookName):
        workbook = openpyxl.Workbook()
        if 'Sheet' in workbook.sheetnames and len(workbook.sheetnames) != 1:
            workbook.remove(workbook['Sheet'])
        workbook.save(workbookName)

    with pandas.ExcelWriter(workbookName, mode='a', if_sheet_exists='replace') as writer:
        dataframe.to_excel(writer, sheet_name=name)

    workbook = openpyxl.load_workbook(workbookName)
    if 'Sheet' in workbook.sheetnames and len(workbook.sheetnames) != 1:
        workbook.remove(workbook['Sheet'])
    for sheet in workbook.worksheets:
        sheet.freeze_panes = 'C2'
        rows = sheet[1]
        for row in rows:
            sheet.column_dimensions[row.column_letter].width = 14
        sheet.column_dimensions['C'].width = 12
        sheet.column_dimensions['A'].width = 45
        sheet.column_dimensions['B'].width = 100
    workbook.save(workbookName)


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

# exit(0)

videoId = extract_playlist(playlist_key=playlistKey)

current_data = get_today_count(videoId)

save_data(current_data, artistName)

for Id in extract_playlist(playlist_key=playlistKey):
    print(Id)
    data = get_view_count_and_data(Id=Id)
    pprint(data)
