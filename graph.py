import os.path
import sqlite3
import pprint
import matplotlib.lines
import numpy
import pandas
import seaborn as sns
import time
import matplotlib.pyplot as plt
import japanize_matplotlib
from matplotlib import spines
from bs4 import BeautifulSoup

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

process_list = [
    ['PLeUX-FlHsb-tGpXYdlTS8rjjqCLxUB-eh', '鈴木愛理'],
    ['PLAAEA82D2950BC77D', 'モーニング娘。'],
    ['PLs8AlpdTjgwdSDETD55q0i3W98tC9SAur', 'Juice=Juice'],
    ['PL04DB1D3D596D47E7', '℃-ute'],
    ['PL0DCF7F78614F3AE6', 'アンジュルム'],
    ['PLF0E7D2433E255B81', 'Buono!'],
    ['OLAK5uy_l_xKCyQPw4uXQd3mnw0yShaZm3AOANkQI', 'Berryz工房'],
    ['PL8m86iV3p-nRdW2cckAwqruBKuzrxoVvW', 'BEYOOOOONDS'],
    ['PLcu1vvKzbBMk1i4k-DF3q5ii0007W-zh7', 'こぶしファクトリー'],
    ['PL0XLej3y4LDmLO0FHu8HBkldiggTt1Es4', 'つばきファクトリー'],
    ['PLhDVFhoEVU3l3X0obfPzdD5OHTbnv7Oio', 'カントリー・ガールズ'],
    ['PLFMni9aeqKTyLxgYVGR9y7zO28Ip5q6Kb', '道重さゆみ'],
    ['PL6A59UsSlG7ex5t5QBIbi4PPviUrZr43p', '宮本佳林'],
    ['PL4CUK5GhdtMnB4ByVY_X3smojU2uY6fAB', 'PINK CRES.'],
    ['PLFMni9aeqKTw_nNHBiGWfPLT-VMdMez97', 'COVERS - One on One -'],
    ['PLFMni9aeqKTwHuSxF4zsHUBMwrubNI05X', 'COVERS ～The Ballad～'],
    ['PLFMni9aeqKTzQ4ciZ-vNscbKge63ohqri', 'アプカミ・ミュージック・デリバリー'],
    ['PLPHwLN81i8cqlVTlXWre1Z7daRXXoa_h_', 'Bitter & Sweet'],
    ['PLFMni9aeqKTwRBEifr0wecspeZPZ24AEN', 'ブラザーズ5'],
    ['PLFMni9aeqKTx6FGeICQu6AMh_h7XaiWrB', 'シャ乱Q'],
    ['PLcDcrjhCHv-3qWE_6ygbLOMQWHgDSGjI5', 'LoVendoЯ'],
    ['PLFMni9aeqKTzQ054kNN0VAn_TC8HVIPvA', '田﨑あさひ'],
    ['PLXok3xPFmG2Akv9qLrdDW1ArlCiodq9Bi', '小片リサ'],
    ['PLXok3xPFmG2ASK8fo_GEwdk7JQALn0P_o', '高橋愛・田中れいな・夏焼雅'],
    ['PLFMni9aeqKTx6nJoI4lDcXIW0RnkIj-WC', '吉川友'],
    ['PL106616353F82EF27', '中島卓偉'],
    ['PLFMni9aeqKTxaQnGrEBaf20ZtWGc2FGGt', 'KAN'],
    ['PLFMni9aeqKTwLp-YS0TdSAJNFp2QdF5et', 'HANGRY&ANGRY'],
    ['PLFMni9aeqKTxigXADUo3SSCv1CdjMk8ua', 'SATOYAMA SATOUMI movement'],
    ['PLFMni9aeqKTyw-UpUPRSEJtD0QfjasWhH', '松原健之'],
    ['PLFMni9aeqKTz7uYHYKB-b_7SRo7dxKmeL', '上々軍団'],
    ['OLAK5uy_m-IDdDas3oTbaeCG8B-EMeQTe7uwW0wcw', '真野恵里菜'],
    ['OLAK5uy_mZKo1FwBv_WzjTnkYLglBj4dlWAuax3Js', '森高千里'],
    ['PL59O0JbKsFLp-RYKpMhN_pooj_bJckLL7', 'アップアップガールズ(仮)'],
    ['OLAK5uy_kFIc8YxoczUnmcpF3Cgrew3HahESCz2ls', '鞘師里保'],
    ['PLFMni9aeqKTwKr8lVnRSCHFcDiQEjFB_v', '犬神サーカス団'],
    ['PLFMni9aeqKTwvVpSgoB9GyIscELI5ECBr', 'つんく♂']
]

# process_list = [
#     ['PLFMni9aeqKTzQ4ciZ-vNscbKge63ohqri', 'アプカミ・ミュージック・デリバリー']
# ]

now = time.time()
db = sqlite3.connect('save.sqlite')
for name in process_list:
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
    print(dataframe)
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
    exportFrame.to_excel('test.xlsx')

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
        dataframe.plot(zorder=1)
        fs *= 3
        handles, labels = plt.gca().get_legend_handles_labels()
        plt.legend(handles[::-1], labels[::-1],
                   bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=fs, ncol=3)
    elif list_len >= 60:
        plt.rcParams["figure.figsize"] = (21, 9)
        dataframe.plot(zorder=1)
        fs *= 2
        handles, labels = plt.gca().get_legend_handles_labels()
        plt.legend(handles[::-1], labels[::-1],
                   bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=fs, ncol=2)
    elif list_len >= 0:
        plt.rcParams["figure.figsize"] = (16, 9)
        dataframe.plot(grid=True, zorder=1)
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
    plt.savefig(os.path.join(os.getcwd(), 'images', name[1] + '_1.png'), dpi=240)
    plt.close()

    # plt.show()
    # print(dataframe.columns)
