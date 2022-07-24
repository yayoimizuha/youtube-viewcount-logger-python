import os

import pandas
import const


def gen_tsv():
    print(os.getcwd())

    for _, i in const.playlists():
        dataframe = pandas.read_excel('save.xlsx', sheet_name=i, index_col=0)

        os.makedirs('tsvs', exist_ok=True)
        dataframe.to_csv(os.path.join(os.getcwd(), 'tsvs', i + '.tsv'), sep='\t')


gen_tsv()
