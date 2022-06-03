import datetime
import os.path
import time
from pprint import pprint
import openpyxl
import pandas
import sqlite3
import tweepy

import const
from tweet import tweet

pandas.options.display.max_rows = None
pandas.options.display.max_columns = None
pandas.options.display.width = 6000
pandas.options.display.max_colwidth = 6000
pandas.options.display.colheader_justify = 'left'


def gen_tweet_text(data):
    if data[1][2] is None:
        data[1][2] = "null"
    if data[1][3] is None:
        data[1][3] = "null"
    if data[2][2] is None:
        data[2][2] = "null"
    if data[2][3] is None:
        data[2][3] = "null"
    return """#hpytvc 昨日からの再生回数: #{artist}
1位: {one_name}\t再生回数:{one_count}回
2位: {two_name}\t再生回数:{two_count}回
3位: {three_name}\t再生回数:{three_count}回""".format(artist=data[0][1],
                                                one_name=data[0][2], one_count=data[0][3],
                                                two_name=data[1][2], two_count=data[1][3],
                                                three_name=data[2][2], three_count=data[2][3])


process_list = const.playlists()

now = time.time()
db = sqlite3.connect('save.sqlite')
for name in process_list:
    dataframe = pandas.read_sql("SELECT * FROM '{name}'".format(name=name[1]), db, index_col='index')
    print('\n\n\n')
    dataframe.replace(0, None, inplace=True)
    sortFrame = pandas.DataFrame(columns=['index', 'artist name', 'title', 'view count', 'last update'])
    for index in dataframe.index:
        Slice = pandas.Series.copy(dataframe.loc[index])
        Slice.dropna(inplace=True)
        if 'タイトル' not in Slice.index:
            continue
        if len(Slice) <= 1:
            continue
        print(len(Slice) - 1, end='\t')
        print(index, name[1], Slice.at['タイトル'], end='\t')
        if len(Slice) == 2:
            print(Slice.iat[-1], Slice.axes[-1][-1])
            sortFrame.loc[index] = [index, name[1], Slice.at['タイトル'], Slice.iat[-1], Slice.axes[-1][-1]]
        else:
            delta = (datetime.date.fromisoformat(dataframe.axes[-1][-1]) - datetime.date.fromisoformat(
                dataframe.axes[-1][-2])).days
            print(delta, end='\t')
            countDelta = Slice.iat[-1] - Slice.iat[-2]
            print(int(countDelta / delta), Slice.axes[-1][-1])

            sortFrame.loc[index] = [index, name[1], Slice.at['タイトル'], int(countDelta / delta), Slice.axes[-1][-1]]
        # print(dataframe.loc[index].axes)
        # print(len(dataframe.loc[index]))
        # print(dataframe.loc[index].iat[-1])
        # print()
    print('\n\n\n\n')
    tweet_data = sortFrame.sort_values('view count', ascending=False)[0:3].values.tolist()
    print(len(gen_tweet_text(tweet_data).encode('utf-8')))
    print(gen_tweet_text(tweet_data))
    try:
        if os.environ['DEBUG'] == 'NO':
            status = tweet(text=gen_tweet_text(tweet_data), name=name[1])
        else:
            status = tweet(text=None)
    except tweepy.TweepyException as e:
        pprint(e, width=100)

print(str(time.time() - now) + 's')
