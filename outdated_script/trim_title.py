import re
from unicodedata import normalize


def trim_title(text, artist_name):
    title_regex_one = r"[\(（]([a-zA-Z\s\[\]\'\"”””“\.…,\/　!！=。@’[°C]・:〜\-])*[\)）]"
    title_regex_two = r"[\s|-][Promotion|Music|Video].*[\s|\-]*|Edit|カバー|[\s|-]*YouTube[\s|\-]*|ver|【セルフカヴァー】" \
                      r"|Promotion|Music|Video"
    title_regex_three = r"[\[\(（]([a-zA-Z\s”\[［\]］\.\/’\'\"&。:〜”“0-9\-=\?!×#~,♂　@（）])*[\]\)）]?"
    title_regex_four = r'※.*'  # r"ショート|Short|short|Version|Ver.|Ver|バージョン|Dance|ダンス|リリック.*|"
    if artist_name == '鞘師里保':
        return re.sub(r'\(.*\)', '', text)
    if artist_name == 'COVERS - One on One -':
        return text
    if artist_name == 'アップアップガールズ(仮)':
        tmp = re.sub(r'【MUSIC VIDEO】|\([A-z\s\[\]\-！!].*\)|ミュージック|イメージ|ビデオ|\[.*?\]', '', text,
                     re.IGNORECASE)
        return re.sub(r'UP|GIRLS|kakko|KARI|MV|MUSIC|VIDEO|（MV）', '', tmp, re.IGNORECASE | re.MULTILINE)
    if artist_name == 'シャ乱Q':
        return re.sub(r'[v|(].*', '', normalize('NFKC', text))
    if artist_name == 'つんく♂' or artist_name == '℃-ute' or artist_name == 'Berryz工房' or artist_name == 'Buono!' \
            or artist_name == 'PINK CRES.' or artist_name == 'こぶしファクトリー' or artist_name == 'ブラザーズ5' \
            or artist_name == '真野恵里菜' or artist_name == '鈴木愛理':
        return re.sub(r'\(.*', '', normalize('NFKC', text))
    if artist_name == 'Bitter & Sweet':
        return re.sub(r'\(.*?\)', '', normalize('NFKC', text))
    if artist_name == 'HANGRY&ANGRY':
        return normalize('NFKC', text).replace('VIDEO CLIP', '')
    if artist_name == 'Juice=Juice' or artist_name == 'アンジュルム' or artist_name == '高橋愛・田中れいな・夏焼雅' \
            or artist_name == 'BEYOOOOONDS' or artist_name == 'モーニング娘。' or artist_name == 'OCHA NORMA':
        return re.sub(r'\(.*?\)|\[.*?]|MV|Promotion|Edit', '', normalize('NFKC', text))
    if artist_name == 'LoVendoЯ':
        return re.sub(r'\(.*|\[.*', '', normalize('NFKC', text))
    if artist_name == '小片リサ':
        return re.sub(r'\-.*', '', normalize('NFKC', text))
    if artist_name == 'ハロプロダンス部':
        return re.sub(r'\(.*?\)', '', normalize('NFKC', text))

    text = str(text).replace('(仮)', '@kari@')
    text = str(text).replace('（仮）', '@kari@')
    text = str(text).replace('℃-ute', '@cute@')
    text = str(text).replace('°C-ute', '@cute@')
    return_code = re.sub(title_regex_four, '',
                         re.sub(title_regex_three, '',
                                re.sub(title_regex_two, '',
                                       re.sub(title_regex_one, ' ', normalize('NFKC', text),
                                              re.IGNORECASE), re.IGNORECASE | re.MULTILINE), re.IGNORECASE),
                         re.IGNORECASE)
    return return_code.replace('@kari@', '(仮)').replace('@cute@', '℃-ute')
