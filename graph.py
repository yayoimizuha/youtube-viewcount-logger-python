import os.path
import sqlite3

import matplotlib.lines
import numpy
import pandas
import seaborn as sns
import time
import matplotlib.pyplot as plt
import japanize_matplotlib
import matplotlib.ticker as ptick

sns.set_palette('colorblind')

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
#     ['PLs8AlpdTjgwdSDETD55q0i3W98tC9SAur', 'Juice=Juice']
# ]

now = time.time()
db = sqlite3.connect('save.sqlite')
for name in process_list:
    dataframe = pandas.read_sql("SELECT * FROM '{name}'".format(name=name[1]), db, index_col='タイトル')
    print('\n\n\n')
    dataframe.replace('hide', 0, inplace=True)
    dataframe.replace(0, numpy.NaN, inplace=True)

    print(dataframe)

    print(dataframe.transpose())
    dataframe = dataframe.transpose()
    print(dataframe.index[1])
    dataframe.drop(index='index', axis=0, inplace=True)
    dataframe = dataframe.astype(float)
    print(dataframe)
    dataframe.interpolate(inplace=True)
    sns.color_palette(n_colors=len(dataframe.columns))
    if None in dataframe.columns:
        dataframe.drop(columns=[None], inplace=True)
    plt.rcParams["figure.figsize"] = (16, 9)
    dataframe.plot()
    fs = int(2160 / (len(dataframe.columns) * 6))
    if fs >= 12:
        fs = 12
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=fs)
    plt.tight_layout()

    # plt.figure(dpi=300)
    plt.savefig(os.path.join(os.getcwd(), 'images', name[1] + '.png'), dpi=240)
    plt.show()
    print(dataframe.columns)
