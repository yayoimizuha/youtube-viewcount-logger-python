from os import path, getcwd
from sqlite3 import connect
from japanize_matplotlib import japanize
from matplotlib import pyplot, rcParams
from pandas import read_sql, Int64Dtype, DataFrame, Series, concat, NA
from datetime import date, timedelta

SQLITE_DATABASE = path.join(getcwd(), 'save.sqlite')

japanize()


def pack_comma(txt: str) -> str:
    return f'\"{txt}\"'


def gen_date_array(begin: str, end: str) -> list[str]:
    for i in range((date.fromisoformat(end) - date.fromisoformat(begin)).days):
        yield (date.fromisoformat(begin) + timedelta(i)).__str__()


def frame_collector() -> dict[str:DataFrame]:
    connector = connect(SQLITE_DATABASE)
    cursor = connector.cursor()
    table_name = [name[0] for name in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
    tables: dict[DataFrame] = {name: read_sql(f"SELECT * FROM {pack_comma(name)}", connector, index_col='index') for
                               name in table_name}

    for dataframe_key in tables.keys():
        column_list = tables[dataframe_key].columns.tolist()[1:]
        index_list = tables[dataframe_key].index.tolist()
        title_list: Series = tables[dataframe_key].loc[:, 'タイトル']
        title_list = title_list.replace('0', None)
        num_arr: DataFrame = tables[dataframe_key][column_list]
        tables[dataframe_key] = DataFrame(num_arr.to_numpy(), columns=column_list, index=index_list, dtype=Int64Dtype())
        tables[dataframe_key].loc[:, 'タイトル'] = title_list
        column_list = ['タイトル'] + [col for col in gen_date_array(column_list[1], column_list[-1])]
        sparse_dataframe = DataFrame(columns=column_list, dtype=Int64Dtype())
        tables[dataframe_key] = concat(objs=[sparse_dataframe, tables[dataframe_key]], join='outer')
        tables[dataframe_key]: DataFrame = tables[dataframe_key].reindex(columns=column_list)
        tables[dataframe_key] = tables[dataframe_key].replace(0, NA)

    return tables


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
