import matplotlib
from dl_fonts import get_emoji_path, get_sans_path

matplotlib.use('module://mplcairo.base')

from graph_gen import frame_collector
from pandas import to_datetime, Int64Dtype, isna
from const import html_base
from matplotlib.font_manager import FontProperties
from os import getcwd
from os.path import join
from budoux import load_default_japanese_parser
from unicodedata import east_asian_width, normalize

print(matplotlib.get_backend())

JP_FP = FontProperties(fname=get_sans_path())
EMOJI_FP = FontProperties(fname=get_emoji_path())


def fold_text(text: str, length: int = 20, delimiter='\n', max_length=70) -> str:
    def count_width(snippet: str) -> int:
        width = 0
        for char in snippet:
            if east_asian_width(char) in 'FWA':
                width += 2
            elif char.islower():
                width += 1
            elif char.isupper():
                width += 2
        return width

    if text.__len__() == 0:
        raise ValueError
    parser = load_default_japanese_parser()
    word_list = parser.parse(text)
    return_string = str()
    for word in word_list:
        if count_width(return_string.split(delimiter)[-1] + word) > length:
            return_string += (delimiter + word)
        else:
            return_string += word
    if count_width(return_string) > max_length:
        while count_width(return_string) > max_length:
            return_string = return_string[:-2]
        return_string += '...'
    return return_string.removeprefix(delimiter)


dataframes = frame_collector()
for key, value in dataframes.items():
    print(key)
    value.set_index('タイトル', inplace=True)
    value.columns = to_datetime(value.columns)
    value = value.astype(float)
    # print(value)
    value.interpolate(inplace=True, method='linear', axis=1)
    value['yesterday_displace'] = value[value.columns[-2]] - value[value.columns[-3]]
    value['today_displace'] = value[value.columns[-2]] - value[value.columns[-3]]
    table_data = value[value.columns[-3:]]
    table_data.loc[table_data['yesterday_displace'] > table_data['today_displace'], 'displace'] = '↘'
    table_data.loc[table_data['yesterday_displace'] < table_data['today_displace'], 'displace'] = '↗'
    table_data.loc[table_data['yesterday_displace'] == table_data['today_displace'], 'displace'] = '➡'
    table_data.loc[isna(table_data['yesterday_displace']) & isna(table_data['today_displace']), 'displace'] = '🆕'
    table_data = table_data.drop(['yesterday_displace'], axis=1)
    table_data = table_data.dropna(subset=table_data.columns[0], axis=0)
    table_data = table_data.sort_values('today_displace', ascending=False, na_position='first')
    table_data.columns = ['{}年{}月{}日'.format(*table_data.columns[0].date().__str__().split('-')), '差分', '前日差']
    table_data[table_data.columns[:2]] = table_data.loc[:, table_data.columns[:2]].round()
    table_data[table_data.columns[:2]] = table_data.loc[:, table_data.columns[:2]].astype(Int64Dtype())
    table_data = table_data.astype(object)
    table_data.index = table_data.index.map(
        lambda x: fold_text(normalize('NFKC', str(x)), length=37, max_length=55, delimiter='--nl--'))
    if table_data.index.__len__() > 15:
        table_data = table_data.loc[table_data.index[:15], :]
    with open(join(getcwd(), 'html', key + '.html'), mode='w', encoding='utf-8') as f:
        f.write(html_base(name=key, content=table_data.to_html(render_links=True, notebook=True, justify='center')))
