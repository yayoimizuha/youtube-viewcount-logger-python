from re import IGNORECASE, sub, MULTILINE
from unicodedata import normalize


def playlists():
    return [
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
        ['PLFMni9aeqKTwRBEifr0wecspeZPZ24AEN', 'ブラザーズ5', True],
        ['PLFMni9aeqKTx6FGeICQu6AMh_h7XaiWrB', 'シャ乱Q', True],
        ['PLFMni9aeqKTxAMChTm-sad305266kliMy', 'LoVendoЯ', True],
        ['PLFMni9aeqKTzQ054kNN0VAn_TC8HVIPvA', '田﨑あさひ', True],
        ['PLXok3xPFmG2Akv9qLrdDW1ArlCiodq9Bi', '小片リサ', True],
        ['PLXok3xPFmG2ASK8fo_GEwdk7JQALn0P_o', '高橋愛・田中れいな・夏焼雅', True],
        ['PLFMni9aeqKTx6nJoI4lDcXIW0RnkIj-WC', '吉川友', True],
        ['PL106616353F82EF27', '中島卓偉', True],
        ['PLFMni9aeqKTxaQnGrEBaf20ZtWGc2FGGt', 'KAN', True],
        ['PLFMni9aeqKTwLp-YS0TdSAJNFp2QdF5et', 'HANGRY&ANGRY', True],
        ['PL6xCFVfh13DFK5Gsv_qy7Rlwcg_gzcf_a', 'SATOYAMA SATOUMI movement', True],
        ['PLFMni9aeqKTyw-UpUPRSEJtD0QfjasWhH', '松原健之', True],
        ['PLFMni9aeqKTz7uYHYKB-b_7SRo7dxKmeL', '上々軍団', True],
        ['OLAK5uy_m-IDdDas3oTbaeCG8B-EMeQTe7uwW0wcw', '真野恵里菜', True],
        ['OLAK5uy_mZKo1FwBv_WzjTnkYLglBj4dlWAuax3Js', '森高千里', True],
        ['PL59O0JbKsFLp-RYKpMhN_pooj_bJckLL7', 'アップアップガールズ(仮)', True],
        ['OLAK5uy_kFIc8YxoczUnmcpF3Cgrew3HahESCz2ls', '鞘師里保', True],
        ['PLFMni9aeqKTwKr8lVnRSCHFcDiQEjFB_v', '犬神サーカス団', True],
        ['PLFMni9aeqKTwvVpSgoB9GyIscELI5ECBr', 'つんく♂', True]
    ]


def playlists():
    return [
        ['PLeUX-FlHsb-tGpXYdlTS8rjjqCLxUB-eh', '鈴木愛理', True],
        ['PLFMni9aeqKTwvVpSgoB9GyIscELI5ECBr', 'つんく♂', True]
    ]


def trim_title(text, artist_name):
    title_regex_one = r"[\(（]([a-zA-Z\s\[\]\'\"”””“\.…,\/　!！=。@’[°C]・:〜\-])*[\)）]"
    title_regex_two = r"[\s|-][Promotion|Music|Video].*[\s|\-]*|Edit|カバー|[\s|-]*YouTube[\s|\-]*|ver|【セルフカヴァー】" \
                      r"|Promotion|Music|Video"
    title_regex_three = r"[\[\(（]([a-zA-Z\s”\[［\]］\.\/’\'\"&。:〜”“0-9\-=\?!×#~,♂　@（）])*[\]\)）]?"
    title_regex_four = r'※.*'  # r"ショート|Short|short|Version|Ver.|Ver|バージョン|Dance|ダンス|リリック.*|"
    if artist_name == '鞘師里保':
        return sub(r'\(.*\)', '', text)
    if artist_name == 'COVERS - One on One -':
        return text
    if artist_name == 'アップアップガールズ(仮)':
        tmp = sub(r'【MUSIC VIDEO】|\([A-z\s\[\]\-！!].*\)|ミュージック|イメージ|ビデオ|\[.*?\]', '', text,
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
        return sub(r'\-.*', '', normalize('NFKC', text))
    if artist_name == 'ハロプロダンス部':
        return sub(r'\(.*?\)', '', normalize('NFKC', text))

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
