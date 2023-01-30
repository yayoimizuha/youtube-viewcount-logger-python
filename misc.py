import os

import pandas
import const


def gen_tsv():
    print(os.getcwd())

    for i in const.playlists():
        dataframe = pandas.read_excel('save.xlsx', sheet_name=i[1], index_col=0)

        os.makedirs('tsvs', exist_ok=True)
        dataframe.to_csv(os.path.join(os.getcwd(), 'tsvs', i[1] + '.tsv'), sep='\t')



with open("test.html","w") as f:
    f.write(const.html_base(name="name",content="content"))