import datetime
import glob
from os.path import exists, join
from os import getcwd, environ
from pprint import pprint
from tweepy import API, OAuth1UserHandler, TweepyException
from const import frame_collector, trim_title, playlists
from pandas import Series
from datetime import datetime

consumer_key = environ['API_KEY']
consumer_secret = environ['API_SECRET']
access_token = environ['ACCESS_TOKEN']
access_token_secret = environ['ACCESS_TOKEN_SECRET']

auth = OAuth1UserHandler(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

api = API(auth)


def tweet(text: str, media: list[str], raw: bool) -> None:
    if raw is True:
        return api.update_status(text)
    if text == '':
        text = "test tweet.\n" + str(datetime.now()) + str(name)
        return api.update_status(text)

    media_ids = [api.media_upload(i).media_id_string for i in media]
    return api.update_status(text, media_ids=media_ids)


tweet(text="以下のサイトでグループごとの再生回数のグラフを見られます！"
           "拡大縮小したり、表示したい曲を選択して表示できたりして、毎日の画像ツイートより見やすくなっています！"
           "https://viewcount-logger-20043.web.app/", raw=True, media=[])

tables = frame_collector()

tweet_content: dict[str, (str, list[str])] = dict()

for key, frame in tables.items():
    print(key)
    if frame.columns.__len__() < 3:
        print('列が少なすぎます。')
        continue
    frame.set_index('タイトル', inplace=True)
    frame = frame.astype(float)
    frame.interpolate(method='linear', inplace=True, axis=1)
    frame = frame.loc[frame.index, frame.columns[-2:]]
    incr: Series = frame.iloc[:, 1] - frame.iloc[:, 0]
    incr = incr.astype(int)
    incr.sort_values(ascending=False, inplace=True)
    print_str = str()
    print_str += f'#hpytvc 昨日からの再生回数: #{key}\n'
    for order, (name, count) in enumerate(list(incr.items())[:min(3, incr.size)]):
        print(str(order + 1) + '位', name, str(count) + '回', sep=' ')
        print_str += f'{order + 1}位:{name} {count}回\n'
    # print(print_str)
    files = list()
    if exists(join(getcwd(), 'table', key + '.png')):
        files.append(join(getcwd(), 'table', key + '.png'))
    if exists(join(getcwd(), 'graph', key + '.png')):
        files.append(join(getcwd(), 'graph', key + '.png'))
    tweet_content[key] = (print_str, files)
    print()

pprint(tweet_content)

for playlist_id, key, is_tweet in playlists():
    if is_tweet:
        try:
            pprint(tweet(*tweet_content[key], raw=False))
        except TweepyException as e:
            print(e)
