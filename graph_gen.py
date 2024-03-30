from os import path, getcwd, makedirs
from matplotlib_fontja import japanize
from matplotlib import pyplot, style
from const import frame_collector, playlists
from pandas import DataFrame, to_datetime, DatetimeIndex
from sys import stderr

# style.use('fast')
japanize()


def graph_gen() -> None:
    dataframes: dict[str:DataFrame] = frame_collector()
    for key, value in dataframes.items():
        print(key)
        value: DataFrame = value
        value.dropna(subset=['タイトル', value.columns[-1]], axis=0, how='any', inplace=True)
        value.sort_values(by=value.columns[-1], inplace=True, ascending=False)
        displacing = value.dropna(axis=1, how='all')
        if displacing.columns.__len__() < 3:
            print(f'列が少なすぎます。-> {key}', file=stderr)
            continue
        displacing.loc[displacing.index, ['today_displace']] = \
            displacing.loc[:, displacing.columns[-1]] - displacing.loc[:, displacing.columns[-2]]
        displacing = displacing[displacing['today_displace'] > displacing.iat[0, -1] / 15]
        if displacing.index.__len__() > 27:
            threshold = displacing.sort_values(by='today_displace', ascending=False).iloc[26, -1]
            displacing = displacing[displacing['today_displace'] > threshold]
        value.drop(index=list(set(value.index) - set(displacing.index)), inplace=True)
        value.set_index('タイトル', inplace=True)
        # print(value)
        value.columns = to_datetime(value.columns)
        value = value.T
        pyplot.rcParams["figure.dpi"] = 240
        pyplot.rcParams["figure.figsize"] = (16, 9)
        pyplot.rcParams["axes.formatter.use_mathtext"] = True
        value.index = value.index.map(lambda x: f"{x.year}/{x.month}/{x.day}")
        value.plot()
        pyplot.legend(loc='upper left', borderaxespad=1)
        pyplot.xlabel('日付')
        pyplot.ylabel('再生回数')
        pyplot.title(filter(lambda x: x.db_key == key, playlists()).__next__().display_name)
        # pyplot.show()
        pyplot.savefig(path.join(getcwd(), 'graph', key + '.png'))
        pyplot.close()


makedirs(path.join(getcwd(), 'graph'), exist_ok=True)
graph_gen()
