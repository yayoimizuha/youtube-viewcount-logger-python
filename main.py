import json
import os
import re
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
_playlistKey = 'PLeUX-FlHsb-tGpXYdlTS8rjjqCLxUB-eh'
_artistName = '鈴木愛理'
workbookName = 'save.xlsx'
process_list = [
    ['PLeUX-FlHsb-tGpXYdlTS8rjjqCLxUB-eh', '鈴木愛理'],
    ['PLAAEA82D2950BC77D', 'モーニング娘。'],
    ['PLs8AlpdTjgwdSDETD55q0i3W98tC9SAur', 'Juice=Juice'],
    ['PL04DB1D3D596D47E7', ' ℃-ute '],
    ['PL0DCF7F78614F3AE6', 'アンジュルム'],
    ['PLF0E7D2433E255B81', 'Buono!'],
    ['OLAK5uy_l_xKCyQPw4uXQd3mnw0yShaZm3AOANkQI', 'Berryz工房'],
    ['PL8m86iV3p-nRdW2cckAwqruBKuzrxoVvW', 'BEYOOOOONDS'],
    ['PLcu1vvKzbBMk1i4k-DF3q5ii0007W-zh7', 'こぶしファクトリー'],
    ['PL0XLej3y4LDmLO0FHu8HBkldiggTt1Es4', 'つばきファクトリー'],
    ['PLhDVFhoEVU3l3X0obfPzdD5OHTbnv7Oio', 'カントリー・ガールズ']
]
count = 0

title_regex_one = r"[\(（]([a-zA-Z\s\[\]\'\"”””“\.…,\/　!！=。’[°C]・:〜\-])*[\)）]"
title_regex_two = r"Promotion Edit"
title_regex_three = r"[\[\(（]([a-zA-Z\s”\[［\]］\.\/’\'&。:〜”“0-9\-=\?!×#~,　（）])*[\]\)）]"
title_regex_four = r''  # r"ショート|Short|short|Version|Ver.|Ver|バージョン|Dance|ダンス|リリック.*|"


def trim_title(text):
    return re.sub(title_regex_four, '',
                  re.sub(title_regex_three, '',
                         re.sub(title_regex_two, '',
                                re.sub(title_regex_one, '', unicodedata.normalize('NFKC', text)))))


def get_view_count_and_data(Id):
    global count
    video_info_raw = youtube.videos().list(part='statistics,snippet',
                                           fields='items(snippet(title,thumbnails(high,maxres)),'
                                                  'statistics/viewCount)',
                                           id=Id).execute()['items']
    video_info = json.loads(unicodedata.normalize('NFKC', json.dumps(video_info_raw)))

    if not video_info:
        return None
    count += 1
    print(count, end='\t')
    print('https://youtu,be/' + Id, end='\t')
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

    # exit(0)

    today = str(datetime.date.today())
    if os.path.isfile(workbookName):
        workbook = openpyxl.load_workbook(workbookName)
    else:
        workbook = openpyxl.Workbook()

    if artistName not in workbook.sheetnames:
        dataframe = pandas.DataFrame([0])
    else:
        dataframe = pandas.read_excel('save.xlsx', sheet_name=artistName, index_col=0)

    if 'タイトル' not in dataframe.columns:
        dataframe['タイトル'] = ''

    if today not in dataframe.columns:
        dataframe[today] = 0

    for Id in extract_playlist(playlist_key=playlistKey):
        # print(Id)
        data = get_view_count_and_data(Id=Id)
        # pprint(data)
        if data is None:
            continue
        image, title, viewCount, url = data
        if url not in dataframe.index.tolist():
            dataframe.loc[url] = 0
            dataframe.at[url, 'タイトル'] = trim_title(title)

        dataframe.at[url, today] = int(viewCount)
    if 0 in dataframe.columns:
        dataframe.drop(0, axis=0, inplace=True)
        dataframe.drop(0, axis=1, inplace=True)

    if not os.path.isfile(workbookName):
        workbook = openpyxl.Workbook()
        if 'Sheet' in workbook.sheetnames and len(workbook.sheetnames) != 1:
            workbook.remove(workbook['Sheet'])
        workbook.save(workbookName)

    with pandas.ExcelWriter(workbookName, mode='a', if_sheet_exists='replace') as writer:
        dataframe.to_excel(writer, sheet_name=artistName)

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

    print(pandas.read_excel('save.xlsx', sheet_name=artistName, index_col=0))


for processes in process_list:
    count = 0
    process_channel(artistName=processes[1], playlistKey=processes[0])
