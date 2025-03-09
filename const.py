import re
from datetime import date, timedelta
from os import getcwd, path, stat
from os.path import isfile, join
from pickle import load, dump
from re import IGNORECASE, sub, MULTILINE
from sqlite3 import connect
from pandas import DataFrame, read_sql, Series, Int64Dtype, NA, concat
from unicodedata import normalize
from typing import Optional
from datetime import datetime, timezone, timedelta


class Playlist:
    def __init__(self, playlist_key: str, db_key: str, hashtag: Optional[str] = None,
                 display_name: Optional[str] = None, is_tweet: bool = True):
        self.playlist_key = playlist_key
        self.db_key = db_key
        if hashtag is None:
            self.hashtag = db_key
        else:
            self.hashtag = hashtag
        if display_name is None:
            self.display_name = db_key
        else:
            self.display_name = display_name
        self.is_tweet = is_tweet

    def __str__(self):
        return str((self.display_name, self.db_key, self.hashtag))

    def __repr__(self):
        return self.__str__()


def playlists() -> list[Playlist]:
    # def playlists():
    #     return [
    #         ['PLeUX-FlHsb-tGpXYdlTS8rjjqCLxUB-eh', '鈴木愛理', True],
    year = str(datetime.now(timezone(timedelta(hours=+9))).year)[2:]

    return [
        # ' <--- youtube playlist key --->  <- group name -> <- hashtag -> <- is tweet? ->'
        Playlist(playlist_key='PLAAEA82D2950BC77D', db_key='モーニング娘。', hashtag='モーニング娘' + year,
                 display_name='モーニング娘。\'' + year),
        Playlist(playlist_key='PL0DCF7F78614F3AE6', db_key='アンジュルム'),
        Playlist(playlist_key='PLs8AlpdTjgwdSDETD55q0i3W98tC9SAur', db_key='juicejuice', display_name='Juice=Juice'),
        Playlist(playlist_key='PL8m86iV3p-nRdW2cckAwqruBKuzrxoVvW', db_key='BEYOOOOONDS'),
        Playlist(playlist_key='PL0XLej3y4LDmLO0FHu8HBkldiggTt1Es4', db_key='つばきファクトリー'),
        Playlist(playlist_key='PLHdMoq6t0XIA5JLPo-SyTTqEByvdu1cGA', db_key='ochanorma', display_name='OCHA NORMA'),
        Playlist(playlist_key='PLc_REKUn8hhDbzMfjnIocF-siMz7TReb4', db_key='rosychronicle',
                 display_name='ロージークロニクル'),
        Playlist(playlist_key='PLCpSIn0xlyXl0ceNf4rBZvmF2njxunqQC', db_key='ハロプロダンス部', is_tweet=False),
        Playlist(playlist_key='PLcu1vvKzbBMk1i4k-DF3q5ii0007W-zh7', db_key='こぶしファクトリー'),
        Playlist(playlist_key='PLhDVFhoEVU3l3X0obfPzdD5OHTbnv7Oio', db_key='カントリー・ガールズ'),
        Playlist(playlist_key='PLCpSIn0xlyXkPMYUoVgHmj3clVnEWxSHz', db_key='Buono!', hashtag='Buono', is_tweet=False),
        Playlist(playlist_key='PLF0E7D2433E255B81', db_key='Buono!', hashtag='Buono'),
        Playlist(playlist_key='OLAK5uy_l_xKCyQPw4uXQd3mnw0yShaZm3AOANkQI', db_key='Berryz工房'),
        Playlist(playlist_key='PL04DB1D3D596D47E7', db_key='℃-ute', hashtag='c_ute'),
        Playlist(playlist_key='PLeUX-FlHsb-tGpXYdlTS8rjjqCLxUB-eh', db_key='鈴木愛理'),
        Playlist(playlist_key='PLFMni9aeqKTyLxgYVGR9y7zO28Ip5q6Kb', db_key='道重さゆみ'),
        Playlist(playlist_key='PL6A59UsSlG7ex5t5QBIbi4PPviUrZr43p', db_key='宮本佳林'),
        Playlist(playlist_key='PL4CUK5GhdtMnB4ByVY_X3smojU2uY6fAB', db_key='PINKCRES', hashtag='PINKCRES',
                 display_name='PINK CRES.', is_tweet=False),
        Playlist(playlist_key='PLCpSIn0xlyXl5zat4Nzwhd-JC5D-QR14d', db_key='COVERS - One on One -',
                 hashtag='CoversOneOnOne', is_tweet=False),
        Playlist(playlist_key='PLFMni9aeqKTw_nNHBiGWfPLT-VMdMez97', db_key='COVERS - One on One -',
                 hashtag='CoversOneOnOne'),
        Playlist(playlist_key='PLFMni9aeqKTwHuSxF4zsHUBMwrubNI05X', db_key='COVERS ～The Ballad～',
                 hashtag='CoversTheBallad'),
        Playlist(playlist_key='PLFMni9aeqKTzQ4ciZ-vNscbKge63ohqri', db_key='アプカミ・ミュージック・デリバリー',
                 is_tweet=False),
        Playlist(playlist_key='PLPHwLN81i8cqlVTlXWre1Z7daRXXoa_h_', db_key='ビタスイ', display_name='Bitter & Sweet'),
        Playlist(playlist_key='PLFMni9aeqKTwRBEifr0wecspeZPZ24AEN', db_key='ブラザーズ5', is_tweet=False),
        Playlist(playlist_key='PLFMni9aeqKTx6FGeICQu6AMh_h7XaiWrB', db_key='シャ乱Q'),
        Playlist(playlist_key='PLFMni9aeqKTxAMChTm-sad305266kliMy', db_key='LoVendoЯ', is_tweet=False),
        Playlist(playlist_key='PLFMni9aeqKTzQ054kNN0VAn_TC8HVIPvA', db_key='田﨑あさひ', is_tweet=False),
        # Playlist(playlist_key='PLXok3xPFmG2Akv9qLrdDW1ArlCiodq9Bi', db_key='小片リサ'),
        Playlist(playlist_key='PLXok3xPFmG2ASK8fo_GEwdk7JQALn0P_o', db_key='高橋愛・田中れいな・夏焼雅',
                 is_tweet=False),
        Playlist(playlist_key='PLFMni9aeqKTx6nJoI4lDcXIW0RnkIj-WC', db_key='吉川友', is_tweet=False),
        Playlist(playlist_key='PL106616353F82EF27', db_key='中島卓偉'),
        Playlist(playlist_key='PLFMni9aeqKTxaQnGrEBaf20ZtWGc2FGGt', db_key='KAN', is_tweet=False),
        Playlist(playlist_key='PLFMni9aeqKTwLp-YS0TdSAJNFp2QdF5et', db_key='hangryangryf',
                 display_name='HANGRY&ANGRY', is_tweet=False),
        Playlist(playlist_key='PL6xCFVfh13DFK5Gsv_qy7Rlwcg_gzcf_a', db_key='里山里海',
                 display_name='SATOYAMA SATOUMI movement'),
        Playlist(playlist_key='PLFMni9aeqKTyw-UpUPRSEJtD0QfjasWhH', db_key='松原健之'),
        Playlist(playlist_key='PLFMni9aeqKTz7uYHYKB-b_7SRo7dxKmeL', db_key='上々軍団', is_tweet=False),
        Playlist(playlist_key='OLAK5uy_m-IDdDas3oTbaeCG8B-EMeQTe7uwW0wcw', db_key='真野恵里菜'),
        Playlist(playlist_key='OLAK5uy_mZKo1FwBv_WzjTnkYLglBj4dlWAuax3Js', db_key='森高千里'),
        Playlist(playlist_key='PL59O0JbKsFLp-RYKpMhN_pooj_bJckLL7', db_key='アップアップガールズ(仮)', hashtag='アプガ',
                 is_tweet=False),
        Playlist(playlist_key='OLAK5uy_kFIc8YxoczUnmcpF3Cgrew3HahESCz2ls', db_key='鞘師里保'),
        Playlist(playlist_key='PLFMni9aeqKTwKr8lVnRSCHFcDiQEjFB_v', db_key='犬神サーカス団', is_tweet=False),
        Playlist(playlist_key='PLFMni9aeqKTwvVpSgoB9GyIscELI5ECBr', db_key='つんく', display_name='つんく♂',
                 is_tweet=False),
        Playlist(playlist_key='PLXok3xPFmG2A9jkc4415xT1t_lTMyTtc3', db_key='佐藤優樹'),
        Playlist(playlist_key='PLFMni9aeqKTwb91a6lLvQiEMNEZXpD88v', db_key='ハロプロ25周年記念公開MV'),
        Playlist(playlist_key='PLFMni9aeqKTw8G3gCcMDBUKwDCAts-Cj-', db_key='松浦亜弥'),
        Playlist(playlist_key='PLFMni9aeqKTxpeBpkYUe4TbQ2RtFiz8hJ', db_key='藤本美貴', is_tweet=False),
        Playlist(playlist_key='PLFMni9aeqKTzwxJrS92a6zbxKQiYydGkG', db_key='後藤真希', is_tweet=False),
        Playlist(playlist_key='PLFMni9aeqKTxJqAbOc60917KKfOsAmjqD', db_key='中澤裕子', is_tweet=False),
        Playlist(playlist_key='PLFMni9aeqKTxNAXGrN4VW_qpYD1fLoI5H', db_key='メロン記念日'),
        Playlist(playlist_key='PLFMni9aeqKTzGddgeMhbXMhXgz8dMgaJs', db_key='太陽とシスコムーン'),
        Playlist(playlist_key='PLXok3xPFmG2DWOqD9q7yGm608F6gNjUIx', db_key='稲場愛香'),
        Playlist(playlist_key='PLXok3xPFmG2DsiyGQD2A5Elihz05RVIR-', db_key='mlinemusic', display_name='M-line Music'),
        Playlist(playlist_key='PLFMni9aeqKTwIf7DShjl6y2Lf2-MGUvd3', db_key='タンポポ', is_tweet=False),
        Playlist(playlist_key='PLFMni9aeqKTw00DcNa2h05AdhzJCr-eiV', db_key='プッチモニ', is_tweet=False),
        Playlist(playlist_key='PLFMni9aeqKTwrRRpwWLL9U7QQqtPZaPS3', db_key='ミニモニ。', hashtag='ミニモニ',
                 is_tweet=False),
        Playlist(playlist_key='PLHBlp1EugxwdY9abMZagocJvRfbc_gVMr', db_key='ME_I', display_name='ME:I')
    ]
    #         ['PLFMni9aeqKTwvVpSgoB9GyIscELI5ECBr', 'つんく♂', True],
    #         ['PLXok3xPFmG2A9jkc4415xT1t_lTMyTtc3', '佐藤優樹', False]
    #     ]


def trim_title(text: str, artist_name: str):
    title_regex_one = r"[\(（]([a-zA-Z\s\[\]\'\"”””“\.…,\/　!！=。@’[°C]・:〜\-])*[\)）]"
    title_regex_two = r"[\s|-][Promotion|Music|Video].*[\s|\-]*|Edit|カバー|[\s|-]*YouTube[\s|\-]*|ver|【セルフカヴァー】" \
                      r"|Promotion|Music|Video"
    title_regex_three = r"[\[\(（]([a-zA-Z\s”\[［\]］\.\/’\'\"&。:〜”“0-9\-=\?!×#~,♂　@（）])*[\]\)）]?"
    title_regex_four = r'※.*'  # r"ショート|Short|short|Version|Ver.|Ver|バージョン|Dance|ダンス|リリック.*|"
    if artist_name == '鞘師里保':
        return sub(r'/.*?$|\(.*?$', '', sub(r'.*?-', '', text))
    if artist_name == 'COVERS - One on One -':
        return text.removeprefix('COVERS - One on One -').removeprefix('COVERS -One on One-')
    if artist_name == 'アップアップガールズ(仮)':
        tmp = sub(r'【MUSIC VIDEO】|\([A-z\s\[\]\-！!].*\)|ミュージック|イメージ|ビデオ|[.*?]', '', text,
                  IGNORECASE)
        return sub(r'UP|GIRLS|kakko|KARI|MV|MUSIC|VIDEO|（MV）', '', tmp, IGNORECASE | MULTILINE)
    if artist_name == 'シャ乱Q':
        return sub(r'[v|(].*', '', normalize('NFKC', text))
    if artist_name == 'つんく♂' or artist_name == '℃-ute' or artist_name == 'Berryz工房' or artist_name == 'Buono!' \
            or artist_name == 'PINK CRES.' or artist_name == 'こぶしファクトリー' or artist_name == 'ブラザーズ5' \
            or artist_name == '真野恵里菜' or artist_name == '鈴木愛理':
        return sub(r'\(.*', '', normalize('NFKC', text))
    if artist_name == 'Bitter & Sweet':
        return sub(r'\(.*?\)', '', normalize('NFKC', text))
    if artist_name == 'HANGRY&ANGRY':
        return normalize('NFKC', text).replace('VIDEO CLIP', '')
    if artist_name == 'Juice=Juice' or artist_name == 'アンジュルム' or artist_name == '高橋愛・田中れいな・夏焼雅' \
            or artist_name == 'BEYOOOOONDS' or artist_name == 'モーニング娘。' or artist_name == 'OCHA NORMA':
        return sub(r'\(.*?\)|\[.*?]|MV|Promotion|Edit', '', normalize('NFKC', text))
    if artist_name == 'LoVendoЯ':
        return sub(r'\(.*|\[.*', '', normalize('NFKC', text))
    if artist_name == '小片リサ':
        return sub(r'-.*', '', normalize('NFKC', text))
    if artist_name == 'ハロプロダンス部':
        return sub(r'\(.*?\)', '', normalize('NFKC', text))
    if artist_name == '佐藤優樹':
        if '-One on One-' in text:
            return text.removeprefix('COVERS -One on One-')
    if artist_name == 'M-line Music':
        return re.sub(r'(」).*|(』).*|COVERS.*- ', r'\1\2', normalize('NFKC', text))

    text = str(text).replace('(仮)', '@kari@')
    text = str(text).replace('（仮）', '@kari@')
    text = str(text).replace('℃-ute', '@cute@')
    text = str(text).replace('°C-ute', '@cute@')
    return_code = sub(title_regex_four, '',
                      sub(title_regex_three, '',
                          sub(title_regex_two, '',
                              sub(title_regex_one, ' ', normalize('NFKC', text),
                                  IGNORECASE), IGNORECASE | MULTILINE), IGNORECASE),
                      IGNORECASE)
    return return_code.replace('@kari@', '(仮)').replace('@cute@', '℃-ute')


def html_base(name: str, content: str) -> str:
    return f"""<!DOCTYPE html>

    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="https://unpkg.com/mvp.css">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300&family=Noto+Sans:wght@300&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Noto+Emoji:wght@700&display=swap" rel="stylesheet">
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

     table thead th:nth-child(n){{
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
        font-size: 20px;
        transform: scale(1.5, 1.5) translateY(25%);
     }}

     table tbody tr td:nth-of-type(1){{
        font-family: 'Noto Sans', sans-serif;
     }}
     table tbody tr td:nth-of-type(2){{
        font-family: 'Noto Sans', sans-serif;
     }}
     table tbody tr td:nth-of-type(3){{
       font-family: 'Noto Emoji', sans-serif;
     }}
     </style>
     <div style="text-align: center;">
        <p style="font-size:30px">
            {name}
        </p>
     </div>
    {content}
        <script>
            let thead = document.getElementsByTagName('thead')
            thead[0].removeChild(thead[0].getElementsByTagName("tr")[1])
            document.getElementsByTagName("th")[0].innerHTML="タイトル"
        </script>
    </body>
    """.replace('--nl--', '<br>')


def pack_comma(txt: str) -> str:
    return f'\"{txt}\"'


def gen_date_array(begin: str, end: str) -> list[str]:
    for i in range((date.fromisoformat(end) - date.fromisoformat(begin)).days + 1):
        yield (date.fromisoformat(begin) + timedelta(i)).__str__()


SQLITE_DATABASE = path.join(getcwd(), 'save.sqlite')


def frame_collector() -> dict[str, DataFrame]:
    if isfile(join(getcwd(), 'frame.pickle')):
        if stat(path=join(getcwd(), 'frame.pickle')).st_mtime > stat(path=join(getcwd(), 'save.sqlite')).st_mtime:
            with open(join(getcwd(), 'frame.pickle'), mode='rb') as f:
                return load(f)

    connector = connect(SQLITE_DATABASE)
    cursor = connector.cursor()
    table_name = [name[0] for name in
                  cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
    tables: dict[str, DataFrame] = {
        name: read_sql(f"SELECT * FROM {pack_comma(name)}", connector, index_col='index')
        for name in table_name}

    for dataframe_key in tables.keys():
        column_list = tables[dataframe_key].columns.tolist()[1:]
        index_list = tables[dataframe_key].index.tolist()
        title_list: Series = tables[dataframe_key].loc[:, 'タイトル']
        title_list = title_list.replace('0', None)
        num_arr: DataFrame = tables[dataframe_key][column_list]
        tables[dataframe_key] = DataFrame(num_arr.to_numpy(), columns=column_list, index=index_list,
                                          dtype=Int64Dtype())
        tables[dataframe_key].loc[:, 'タイトル'] = title_list
        column_list = ['タイトル'] + [col for col in gen_date_array(column_list[0], column_list[-1])]
        sparse_dataframe = DataFrame(columns=column_list, dtype=Int64Dtype())
        tables[dataframe_key] = concat(objs=[sparse_dataframe, tables[dataframe_key]], join='outer')
        tables[dataframe_key]: DataFrame = tables[dataframe_key].reindex(columns=column_list)
        tables[dataframe_key] = tables[dataframe_key].replace(0, NA)

    connector.close()

    with open(join(getcwd(), 'frame.pickle'), mode='wb') as f:
        dump(tables, f)

    return tables
