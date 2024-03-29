import datetime
from os.path import exists, join
from os import getcwd, environ
from pprint import pprint
from const import playlists, frame_collector
from pandas import Series
from datetime import datetime


def generate_txt() -> dict[str, (str, list[str])]:
    MEDAL: list = ['🥇', '🥈', '🥉']

    tables = frame_collector()

    content: dict[str, (str, list[str])] = dict()

    for key, frame in tables.items():
        # print(key)
        if frame.columns.__len__() < 3:
            print('列が少なすぎます。')
            continue
        frame.set_index('タイトル', inplace=True)
        frame = frame.astype(float)
        frame.interpolate(method='linear', inplace=True, axis=1)
        frame = frame.loc[frame.index, frame.columns[-2:]]
        incr: Series = frame.iloc[:, 1] - frame.iloc[:, 0]
        incr.dropna(inplace=True)
        incr = incr.astype(int)
        incr.sort_values(ascending=False, inplace=True)
        incr = incr[~incr.index.duplicated(keep='first')]
        print_str = str()
        print_str += f'#hpytvc 昨日からの再生回数: #{key}\n'
        for order, (name, count) in enumerate(list(incr.items())[:min(3, incr.size)]):
            # print(MEDAL[order], name, str(count) + '回', sep=' ')
            print_str += f'{MEDAL[order]}{name} {count}回\n'
        # print(print_str)
        files = list()
        if exists(join(getcwd(), 'table', key + '.png')):
            files.append(join(getcwd(), 'table', key + '.png'))
        if exists(join(getcwd(), 'graph', key + '.png')):
            files.append(join(getcwd(), 'graph', key + '.png'))
        content[key] = (print_str, files)
        # print()
    return content


if __name__ == '__main__':

    from tweepy import API, OAuth1UserHandler, TweepyException, Client, Response

    tweet_counter = 0


    def tweet(text: str, media: list[str], v1: API, v2: Client, raw: bool, name: str = "") -> Response:
        global tweet_counter
        tweet_counter += 1
        if raw is True:
            return v2.create_tweet(text=text)
        if text == '':
            text = "test tweet.\n" + str(datetime.now()) + str(name)
            return v2.create_tweet(text=text)

        media_ids = [v1.media_upload(i).media_id_string for i in media]
        return v2.create_tweet(text=text, media_ids=media_ids)


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

    v1_api = API(auth)
    v2_api = Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    tweet_content = generate_txt()

    pprint(tweet_content)

    tweet(text="毎日の最新データはこちらから👉https://github.com/yayoimizuha/youtube-viewcount-logger-python/releases/latest"
               "以下のサイトでグループごとの再生回数のグラフを見られます！"
               "拡大縮小したり、表示したい曲を選択して表示できたりして、毎日の画像ツイートより見やすくなっています！"
               "https://viewcount-logger-20043.web.app/", raw=True, media=[], v1=v1_api, v2=v2_api)

    for playlist_id, key, is_tweet in playlists():
        if is_tweet:
            try:
                if tweet_counter > 50:
                    print("tweet limit exceeded!!")
                    break
                pprint(tweet(*tweet_content[key], raw=False, v1=v1_api, v2=v2_api))
            except TweepyException as e:
                print(e)
