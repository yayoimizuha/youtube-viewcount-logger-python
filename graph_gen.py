from os import path, getcwd
from japanize_matplotlib import japanize
from matplotlib import pyplot
from const import frame_collector
from pandas import DataFrame, to_datetime

japanize()


def graph_gen() -> None:
    dataframes: dict[str:DataFrame] = frame_collector()
    for key, value in dataframes.items():
        value: DataFrame = value
        value.dropna(subset=['タイトル', value.columns[-1]], axis=0, how='any', inplace=True)
        value.sort_values(by=value.columns[-1], inplace=True, ascending=False)
        displacing = value.dropna(axis=1, how='all')
        if displacing.columns.__len__() < 3: continue
        displacing.loc[:, 'today_displace'] = \
            displacing.loc[:, displacing.columns[-1]] - displacing.loc[:, displacing.columns[-2]]
        displacing = displacing[displacing['today_displace'] > displacing.iat[0, -1] / 15]
        if displacing.index.__len__() > 27:
            threshold = displacing.sort_values(by='today_displace', ascending=False).iloc[26, -1]
            displacing = displacing[displacing['today_displace'] > threshold]
        value.drop(index=set(value.index) - set(displacing.index), inplace=True)
        value.set_index('タイトル', inplace=True)
        print(value)
        value.columns = to_datetime(value.columns)
        value = value.T
        pyplot.rcParams["figure.dpi"] = 240
        pyplot.rcParams["figure.figsize"] = (16, 9)
        pyplot.rcParams["axes.formatter.use_mathtext"] = True
        value.plot()
        pyplot.legend(loc='upper left', borderaxespad=1)
        pyplot.xlabel('日付')
        pyplot.ylabel('再生回数')
        pyplot.title(key)
        # pyplot.show()
        pyplot.savefig(path.join(getcwd(), "graph", key + '.png'))
        pyplot.close()
