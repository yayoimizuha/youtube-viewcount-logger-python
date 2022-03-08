import datetime
import os.path
import time
from pprint import pprint
import openpyxl
import pandas
import sqlite3

import tweepy

from tweet import tweet

pandas.options.display.max_rows = None
pandas.options.display.max_columns = None
pandas.options.display.width = 6000
pandas.options.display.max_colwidth = 6000
pandas.options.display.colheader_justify = 'left'


# workbook = openpyxl.load_workbook('save.xlsx')
#
# now = time.time()
# connector = sqlite3.connect('save.sqlite')
# for sheet in workbook.sheetnames:
#     dataframe = pandas.read_excel('save.xlsx', sheet_name=sheet, index_col=0)
#     dataframe.to_excel('tmp.xlsx', sheet_name=sheet)
#     print(sheet)
#     dataframe.to_sql(sheet, connector, if_exists='replace')
#     print(dataframe)
# print(time.time() - now)
# print('\n\n\n')
# connector.close()
#
# now = time.time()
# for page in workbook.sheetnames:
#     connector = sqlite3.connect('save.sqlite')
#     saver = sqlite3.connect('test.sqlite')
#     dataframe = pandas.read_sql("SELECT * FROM '{name}'".format(name=page), connector, index_col='タイトル')
#     dataframe.to_sql(page, saver, if_exists='replace')
#     saver.close()
#     connector.close()
#     print(page)
#     # print(dataframe)
#
# print(time.time() - now)
def gen_tweet_text(data):
    return """#hpytvc 昨日からの再生回数: #{artist}
1位: {one_name}\t再生回数:{one_count}回
2位: {two_name}\t再生回数:{two_count}回
3位: {three_name}\t再生回数:{three_count}回""".format(artist=data[0][1],
                                                one_name=data[0][2], one_count=data[0][3],
                                                two_name=data[1][2], two_count=data[1][3],
                                                three_name=data[2][2], three_count=data[2][3])


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
now = time.time()
db = sqlite3.connect('save.sqlite')
for name in process_list:
    dataframe = pandas.read_sql("SELECT * FROM '{name}'".format(name=name[1]), db, index_col='index')
    print('\n\n\n')
    dataframe.replace(0, None, inplace=True)
    sortFrame = pandas.DataFrame(columns=['index', 'artist name', 'title', 'view count', 'last update'])
    for index in dataframe.index:
        Slice = pandas.Series.copy(dataframe.loc[index])
        Slice.dropna(inplace=True)
        if 'タイトル' not in Slice.index:
            continue
        if len(Slice) <= 1:
            continue
        print(len(Slice) - 1, end='\t')
        print(index, name[1], Slice.at['タイトル'], end='\t')
        if len(Slice) == 2:
            print(Slice.iat[-1], Slice.axes[-1][-1])
            sortFrame.loc[index] = [index, name[1], Slice.at['タイトル'], Slice.iat[-1], Slice.axes[-1][-1]]
        else:
            delta = (datetime.date.fromisoformat(dataframe.axes[-1][-1]) - datetime.date.fromisoformat(
                dataframe.axes[-1][-2])).days
            print(delta, end='\t')
            countDelta = Slice.iat[-1] - Slice.iat[-2]
            print(int(countDelta / delta), Slice.axes[-1][-1])

            sortFrame.loc[index] = [index, name[1], Slice.at['タイトル'], int(countDelta / delta), Slice.axes[-1][-1]]
        # print(dataframe.loc[index].axes)
        # print(len(dataframe.loc[index]))
        # print(dataframe.loc[index].iat[-1])
        # print()
    print('\n\n\n\n')
    tweet_data = sortFrame.sort_values('view count', ascending=False)[0:3].values.tolist()
    print(len(gen_tweet_text(tweet_data).encode('utf-8')))
    print(gen_tweet_text(tweet_data))
    try:
        status = tweet(text=gen_tweet_text(tweet_data))
    except tweepy.TweepyException as e:
        pprint(e, width=100)

print(str(time.time() - now) + 's')
