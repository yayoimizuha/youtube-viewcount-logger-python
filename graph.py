import os.path
import sqlite3
import pprint
import numpy
import pandas
import seaborn as sns
import time
import matplotlib.pyplot as plt
import japanize_matplotlib
from bs4 import BeautifulSoup
import const

sns.set()
sns.set_palette('colorblind')
# sns.set_context("paper")
japanize_matplotlib.japanize()

pandas.options.display.max_rows = None
pandas.options.display.max_columns = None
pandas.options.display.width = 6000
pandas.options.display.max_colwidth = 6000
pandas.options.display.colheader_justify = 'left'

html_base = """<!DOCTYPE html>

<head>
  <link rel="stylesheet" href="https://unpkg.com/mvp.css">
  <script src="https://twemoji.maxcdn.com/v/latest/twemoji.min.js" crossorigin="anonymous"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300&family=Noto+Sans:wght@300&display=swap" rel="stylesheet">
</head>

<body>
 <style>  img {{
    width: 30px;
    height: 30px;
    margin-left: 0px;
    margin-top: 5px;
 }}
 
 tr:first-child{{
     white-space: nowrap;
 }}
 
 table thead th:first-child{{
    text-align: center;
 }}
 
 div{{
    margin: auto;
 }}
 
 table{{
    margin: auto;
    margin-top: 7px;
    display: table;
    margin-bottom: 30px;
 }}
 
 body {{
    --color: #118bee;
    --color-accent: #118bee15;
    --color-bg: #fff;
    --color-bg-secondary: #e9e9e9;
    --color-link: #118bee;
    --color-secondary: #920de9;
    --color-secondary-accent: #920de90b;
    --color-shadow: #f4f4f4;
    --color-table: #118bee;
    --color-text: #000;
    --color-text-secondary: #999;
    font-family: 'Noto Sans JP', sans-serif;
    font-family: 'Noto Sans', sans-serif;
    font-size: 20px;
       
 }}
 </style>
 <div style="text-align: center;">
    <p style="font-size:30px">
        {name}
    </p>
 </div>
{content}
 <script>
     twemoji.parse(document.body);
 </script>
</body>
"""

process_list = const.playlists()

# process_list = [
#     ['PL0XLej3y4LDmLO0FHu8HBkldiggTt1Es4', 'つばきファクトリー']
# ]

now = time.time()
db = sqlite3.connect('save.sqlite')
for name in process_list:
    if not name[2]:
        continue
    dataframe = pandas.read_sql("SELECT * FROM '{name}'".format(name=name[1]), db, index_col='タイトル')
    print('\n\n\n')
    dataframe.replace('hide', 0, inplace=True)
    print(dataframe.columns[-1])
    for rows in dataframe.columns:
        if rows == 'index':
            pass
        elif (dataframe[rows] == 0).all():
            dataframe.drop(rows, axis=1, inplace=True)
            print(rows)
        else:
            break
    # print(dataframe)
    dataframe.replace(0, numpy.NaN, inplace=True)

    dataframe.sort_values(dataframe.columns[-1], inplace=True, ascending=True, na_position='first')
    exportFrame = dataframe.transpose().drop(index='index', axis=0).astype(float).interpolate() \
        .transpose().fillna(0).astype(int)
    print(exportFrame.iloc[:, -1] - exportFrame.iloc[:, -2])
    print(exportFrame.iloc[:, -1])
    # exportFrame = pandas.DataFrame(exportFrame.iloc[:, -1] - exportFrame.iloc[:, -2], exportFrame.iloc[:, -1])
    exportFrame = pandas.concat([exportFrame.iloc[:, -1], exportFrame.iloc[:, -1] - exportFrame.iloc[:, -2],
                                 exportFrame.iloc[:, -1] - exportFrame.iloc[:, -2]
                                 - exportFrame.iloc[:, -2] + exportFrame.iloc[:, -3]], axis=1)
    # exportFrame.drop(columns=['タイトル'], inplace=True, axis=1)
    # exportFrame = exportFrame.sort_values(exportFrame.columns[-1], inplace=True, na_position='first')
    print(exportFrame.columns)
    pprint.pprint(exportFrame.index.tolist(), width=200)
    exportFrame = pandas.DataFrame(exportFrame)
    exportFrame.sort_values(exportFrame.columns[1], inplace=True, ascending=False, na_position='first')
    exportFrame.drop(index=[], inplace=True)

    if None in exportFrame.index:
        exportFrame.drop(index=[None], inplace=True)

    print(exportFrame[exportFrame[1] < 0])
    exportFrame.loc[exportFrame[1] < 0, 2] = '↘'
    exportFrame.loc[exportFrame[1] == 0, 2] = '➡'
    exportFrame.loc[exportFrame[1] > 0, 2] = '↗'
    exportFrame.drop(columns=1, inplace=True)

    html_file = html_base.format(content=exportFrame.to_html(render_links=True, notebook=True, justify='center'),
                                 name=name[1])
    soup = BeautifulSoup(html_file, 'html.parser')
    soup.find('thead').find_all('tr')[1].decompose()
    soup.find('thead').find_all('th')[0].insert(2, 'タイトル')

    soup.find_all('style')[1].decompose()

    soup.find('thead').find_all('th')[2].clear()
    soup.find('thead').find_all('th')[2].insert(0, '差分')

    soup.find('thead').find_all('th')[3].clear()
    soup.find('thead').find_all('th')[3].insert(0, '前日差')

    # del soup.find('thead').find('tr').attrs['style']
    html_file = soup.prettify()
    os.makedirs('html', exist_ok=True)
    with open(os.path.join(os.getcwd(), 'html', name[1] + '.html'), mode='w', encoding='utf-8') as f:
        f.write(html_file)
    # print(dataframe)

    # print(dataframe.transpose())
    dataframe = dataframe.transpose()
    print(dataframe.index[1])
    dataframe.drop(index='index', axis=0, inplace=True)
    dataframe = dataframe.astype(float)
    dataframe.interpolate(inplace=True)
    sns.color_palette(n_colors=len(dataframe.columns))

    if None in dataframe.columns:
        dataframe.drop(columns=[None], inplace=True)

    str_len_lim = 25
    list_len = 0
    for string in dataframe.columns:
        dataframe.rename(
            columns={string: '\n'.join([string[i:i + str_len_lim] for i in range(0, len(string), str_len_lim)])},
            inplace=True)
        list_len += len([string[i:i + str_len_lim] for i in range(0, len(string), str_len_lim)])
    print(list_len, len(dataframe.columns))

    fs = int(2160 / (list_len * 6))
    print(fs)
    if fs >= 12:
        fs = 12
    if fs <= 2:
        fs = 2

    if list_len >= 120:
        plt.rcParams["figure.figsize"] = (26, 9)
        dataframe.plot(zorder=1, grid=True, marker='.', markersize='1', markevery=int(len(dataframe.index) / 100) + 1)
        fs *= 3
        handles, labels = plt.gca().get_legend_handles_labels()
        plt.legend(handles[::-1], labels[::-1],
                   bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=fs, ncol=3)
    elif list_len >= 60:
        plt.rcParams["figure.figsize"] = (21, 9)
        dataframe.plot(zorder=1, grid=True, marker='.', markersize='1', markevery=int(len(dataframe.index) / 100) + 1)
        fs *= 2
        handles, labels = plt.gca().get_legend_handles_labels()
        plt.legend(handles[::-1], labels[::-1],
                   bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=fs, ncol=2)
    elif list_len >= 0:
        plt.rcParams["figure.figsize"] = (16, 9)
        dataframe.plot(zorder=1, grid=True, marker='.', markersize='1', markevery=int(len(dataframe.index) / 100) + 1)
        handles, labels = plt.gca().get_legend_handles_labels()
        plt.legend(handles[::-1], labels[::-1],
                   bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=fs)
    plt.xlabel('日付')
    plt.ylabel('再生回数(回)')
    plt.title(name[1])
    plt.grid(linestyle='dashed', color='lightcyan')
    # plt.tick_params(labelbottom=True)
    plt.axhline(y=0, color='black', zorder=-1)
    plt.axvline(x=0, color='black', zorder=-1)
    # plt.plot([dataframe[0], dataframe[0]], [0, 0], "red", linestyle='dashed')

    plt.gca().spines['bottom'].set_visible(True)

    plt.ticklabel_format(style='plain', axis='y')
    plt.tight_layout()
    # plt.figure(dpi=300)
    os.makedirs('images', exist_ok=True)
    plt.savefig(os.path.join(os.getcwd(), 'images', name[1] + '_1.png'), dpi=240)
    plt.close()
    print(len(dataframe.index))

    # plt.show()
    # print(dataframe.columns)
