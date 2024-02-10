import re
from datetime import date, timedelta
from os import getcwd, path, stat
from os.path import isfile, join
from pickle import load, dump
from re import IGNORECASE, sub, MULTILINE
from sqlite3 import connect
from pandas import DataFrame, read_sql, Series, Int64Dtype, NA, concat
from unicodedata import normalize


def playlists():
    return [
        # ' <--- youtube playlist key --->  <- group name -> <- is tweet? ->'
        ['PLAAEA82D2950BC77D', 'モーニング娘。', True],
        ['PL0DCF7F78614F3AE6', 'アンジュルム', True],
        ['PLs8AlpdTjgwdSDETD55q0i3W98tC9SAur', 'Juice=Juice', True],
        ['PL8m86iV3p-nRdW2cckAwqruBKuzrxoVvW', 'BEYOOOOONDS', True],
        ['PL0XLej3y4LDmLO0FHu8HBkldiggTt1Es4', 'つばきファクトリー', True],
        ['PLHdMoq6t0XIA5JLPo-SyTTqEByvdu1cGA', 'OCHA NORMA', True],
        ['PLCpSIn0xlyXl0ceNf4rBZvmF2njxunqQC', 'ハロプロダンス部', True],
        ['PLcu1vvKzbBMk1i4k-DF3q5ii0007W-zh7', 'こぶしファクトリー', True],
        ['PLhDVFhoEVU3l3X0obfPzdD5OHTbnv7Oio', 'カントリー・ガールズ', True],
        ['PLCpSIn0xlyXkPMYUoVgHmj3clVnEWxSHz', 'Buono!', False],
        # 初恋サイダー / Buono! (Live at 日本武道館 2016/8/25)　『Buono! Festa 2016』2016年11月23日にDVDとBlu-rayを同日発売!! を追加
        ['PLF0E7D2433E255B81', 'Buono!', True],
        ['OLAK5uy_l_xKCyQPw4uXQd3mnw0yShaZm3AOANkQI', 'Berryz工房', True],
        ['PL04DB1D3D596D47E7', '℃-ute', True],
        ['PLeUX-FlHsb-tGpXYdlTS8rjjqCLxUB-eh', '鈴木愛理', True],
        ['PLFMni9aeqKTyLxgYVGR9y7zO28Ip5q6Kb', '道重さゆみ', True],
        ['PL6A59UsSlG7ex5t5QBIbi4PPviUrZr43p', '宮本佳林', True],
        ['PL4CUK5GhdtMnB4ByVY_X3smojU2uY6fAB', 'PINK CRES.', True],
        ['PLCpSIn0xlyXl5zat4Nzwhd-JC5D-QR14d', 'COVERS - One on One -', False],
        # COVERS -One on One- ほたる祭りの日 佐藤優樹 x 宮本佳林 (ジュリン) を追加
        ['PLFMni9aeqKTw_nNHBiGWfPLT-VMdMez97', 'COVERS - One on One -', True],
        ['PLFMni9aeqKTwHuSxF4zsHUBMwrubNI05X', 'COVERS ～The Ballad～', True],
        ['PLFMni9aeqKTzQ4ciZ-vNscbKge63ohqri', 'アプカミ・ミュージック・デリバリー', True],
        ['PLPHwLN81i8cqlVTlXWre1Z7daRXXoa_h_', 'Bitter & Sweet', True],
        ['PLFMni9aeqKTwRBEifr0wecspeZPZ24AEN', 'ブラザーズ5', False],
        ['PLFMni9aeqKTx6FGeICQu6AMh_h7XaiWrB', 'シャ乱Q', True],
        ['PLFMni9aeqKTxAMChTm-sad305266kliMy', 'LoVendoЯ', False],
        ['PLFMni9aeqKTzQ054kNN0VAn_TC8HVIPvA', '田﨑あさひ', True],
        ['PLXok3xPFmG2Akv9qLrdDW1ArlCiodq9Bi', '小片リサ', True],
        ['PLXok3xPFmG2ASK8fo_GEwdk7JQALn0P_o', '高橋愛・田中れいな・夏焼雅', False],
        ['PLFMni9aeqKTx6nJoI4lDcXIW0RnkIj-WC', '吉川友', False],
        ['PL106616353F82EF27', '中島卓偉', True],
        ['PLFMni9aeqKTxaQnGrEBaf20ZtWGc2FGGt', 'KAN', False],
        ['PLFMni9aeqKTwLp-YS0TdSAJNFp2QdF5et', 'HANGRY&ANGRY', False],
        ['PL6xCFVfh13DFK5Gsv_qy7Rlwcg_gzcf_a', 'SATOYAMA SATOUMI movement', True],
        ['PLFMni9aeqKTyw-UpUPRSEJtD0QfjasWhH', '松原健之', True],
        ['PLFMni9aeqKTz7uYHYKB-b_7SRo7dxKmeL', '上々軍団', False],
        ['OLAK5uy_m-IDdDas3oTbaeCG8B-EMeQTe7uwW0wcw', '真野恵里菜', True],
        ['OLAK5uy_mZKo1FwBv_WzjTnkYLglBj4dlWAuax3Js', '森高千里', True],
        ['PL59O0JbKsFLp-RYKpMhN_pooj_bJckLL7', 'アップアップガールズ(仮)', True],
        ['OLAK5uy_kFIc8YxoczUnmcpF3Cgrew3HahESCz2ls', '鞘師里保', True],
        ['PLFMni9aeqKTwKr8lVnRSCHFcDiQEjFB_v', '犬神サーカス団', False],
        ['PLFMni9aeqKTwvVpSgoB9GyIscELI5ECBr', 'つんく♂', False],
        ['PLXok3xPFmG2A9jkc4415xT1t_lTMyTtc3', '佐藤優樹', True],
        ['PLFMni9aeqKTwb91a6lLvQiEMNEZXpD88v', 'ハロプロ25周年記念公開MV', True],
        ['PLFMni9aeqKTw8G3gCcMDBUKwDCAts-Cj-', '松浦亜弥', True],
        ['PLFMni9aeqKTxpeBpkYUe4TbQ2RtFiz8hJ', '藤本美貴', False],
        ['PLFMni9aeqKTzwxJrS92a6zbxKQiYydGkG', '後藤真希', False],
        ['PLFMni9aeqKTxJqAbOc60917KKfOsAmjqD', '中澤裕子', False],
        ['PLFMni9aeqKTxNAXGrN4VW_qpYD1fLoI5H', 'メロン記念日', True],
        ['PLFMni9aeqKTzGddgeMhbXMhXgz8dMgaJs', '太陽とシスコムーン', True],
        ['PLXok3xPFmG2DWOqD9q7yGm608F6gNjUIx', '稲場愛香', True],
        ['PLXok3xPFmG2DsiyGQD2A5Elihz05RVIR-', 'M-line Music', True],
        ['PLFMni9aeqKTwIf7DShjl6y2Lf2-MGUvd3', 'タンポポ', False],
        ['PLFMni9aeqKTw00DcNa2h05AdhzJCr-eiV', 'プッチモニ', False],
        ['PLFMni9aeqKTwrRRpwWLL9U7QQqtPZaPS3', 'ミニモニ。', False]
    ]


# def playlists():
#     return [
#         ['PLeUX-FlHsb-tGpXYdlTS8rjjqCLxUB-eh', '鈴木愛理', True],
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
    table_name = [name[0] for name in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
    tables: dict[str, DataFrame] = {name: read_sql(f"SELECT * FROM {pack_comma(name)}", connector, index_col='index')
                                    for name in table_name}

    for dataframe_key in tables.keys():
        column_list = tables[dataframe_key].columns.tolist()[1:]
        index_list = tables[dataframe_key].index.tolist()
        title_list: Series = tables[dataframe_key].loc[:, 'タイトル']
        title_list = title_list.replace('0', None)
        num_arr: DataFrame = tables[dataframe_key][column_list]
        tables[dataframe_key] = DataFrame(num_arr.to_numpy(), columns=column_list, index=index_list, dtype=Int64Dtype())
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
