from pandas import read_sql, NA, Int64Dtype, DataFrame, Series
from sqlite3 import connect
from os import path, getcwd
from numpy import int64, where, NAN
from numba import njit, i8

SQLITE_DATABASE = path.join(getcwd(), 'save.sqlite')


def pack_comma(txt: str) -> str:
    return f'\"{txt}\"'


@njit(i8[:, :](i8[:, :]), cache=True)
def fill_first_na(arr):
    for index in range(arr.shape[0]):
        if arr[index][0] != -1:
            continue
        else:
            arr[index][where(arr[index] != -1)[0][0] - 1] = 0
    return arr


def main():
    connector = connect(SQLITE_DATABASE)
    cursor = connector.cursor()
    table_name = [name[0] for name in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
    tables = {name: read_sql(f"SELECT * FROM {pack_comma(name)}", connector, index_col='index') for name in table_name}

    for dataframe_key in tables.keys():
        column_list = tables[dataframe_key].columns.tolist()[1:]
        index_list = tables[dataframe_key].index.tolist()
        title_list: Series = tables[dataframe_key].loc[:, 'タイトル']
        title_list = title_list.replace('0', None)
        num_arr: DataFrame = tables[dataframe_key][column_list]
        num_arr = num_arr.replace(NAN, -1)
        num_arr = num_arr.astype(int64)
        num_arr = fill_first_na(num_arr.to_numpy(copy=True, na_value=-1))
        tables[dataframe_key] = DataFrame(num_arr, columns=column_list, index=index_list, dtype=Int64Dtype())
        tables[dataframe_key].replace(-1, NA, inplace=True)
        tables[dataframe_key].loc[:, 'タイトル'] = title_list
        column_list = ['タイトル'] + column_list
        tables[dataframe_key] = tables[dataframe_key].reindex(columns=column_list)


main()
