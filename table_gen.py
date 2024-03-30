import os
from pickle import dump
from multiprocessing import Process
from sys import stdout, stderr
from subprocess import run
from pandas import to_datetime, Int64Dtype, isna, concat, NA
from const import html_base, frame_collector, playlists
from os import getcwd, makedirs
from os.path import join
from budoux import load_default_japanese_parser
from unicodedata import east_asian_width, normalize
from PIL import Image
from PIL.ImageChops import difference

if os.name == 'nt':
    firefox_path = r"C:\Program Files\Firefox Developer Edition\firefox.exe"
else:
    firefox_path = "/opt/firefox/firefox"


def http_server() -> None:
    from http.server import HTTPServer, SimpleHTTPRequestHandler

    class SimpleServer(SimpleHTTPRequestHandler, object):
        def do_GET(self) -> None:
            super(SimpleServer, self).do_GET()

    with HTTPServer(server_address=('localhost', 8888), RequestHandlerClass=SimpleServer) as httpd:
        httpd.serve_forever()


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
        return ""
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


def crop(file_key: str) -> None:
    img = Image.open(fp=join(getcwd(), 'table', f'{file_key}.png')).convert('RGB')
    white = Image.new(mode='RGB', size=img.size, color='white')
    diff = difference(img, white)
    crop_range = diff.convert('RGB').getbbox()
    margin = Image.new(mode='RGB', size=(crop_range[2] - crop_range[0] + 100, crop_range[3] - crop_range[1] + 100),
                       color='white')
    margin.paste(img.crop(crop_range), (50, 50))
    margin.save(join(getcwd(), 'table', f'{file_key}.png'))


makedirs(join(getcwd(), 'html'), exist_ok=True)
makedirs(join(getcwd(), 'table'), exist_ok=True)

markdown_dict = dict()

if __name__ == '__main__':

    serve = Process(target=http_server, daemon=True)
    serve.start()

    dataframes = frame_collector()
    for key, value in dataframes.items():
        print(key)
        if value.columns.__len__() < 4:
            print('列が少なすぎます。', file=stderr)
            continue
        value.set_index('タイトル', inplace=True)
        value.columns = to_datetime(value.columns)
        value[value.columns] = value[value.columns].astype(float)
        # print(value)
        value[value.columns].interpolate(inplace=True, method='linear', axis=1)
        value = concat([value, (value[value.columns[-2]] - value[value.columns[-3]]).rename('yesterday_displace')],
                       axis=1)
        value = concat([value, (value[value.columns[-2]] - value[value.columns[-3]]).rename('today_displace')], axis=1)
        table_data = value[value.columns[-3:]]
        # table_data = table_data.astype(object)
        table_data = table_data.assign(displace="")
        table_data.loc[table_data['yesterday_displace'] > table_data['today_displace'], ['displace']] = '↘'
        table_data.loc[table_data['yesterday_displace'] < table_data['today_displace'], ['displace']] = '↗'
        table_data.loc[table_data['yesterday_displace'] == table_data['today_displace'], ['displace']] = '➡'
        table_data.loc[isna(table_data['yesterday_displace']) & isna(table_data['today_displace']), 'displace'] = '🆕'
        table_data = table_data.drop(['yesterday_displace'], axis=1)
        table_data = table_data.dropna(subset=table_data.columns[0], axis=0)
        table_data = table_data.sort_values('today_displace', ascending=False, na_position='first')
        table_data.columns = [
            '{}年{}月{}日時点--nl--での総再生回数'.format(*table_data.columns[0].date().__str__().split('-')),
            '昨日からの--nl--再生回数', '前日比']
        table_data[table_data.columns[:2]] = table_data.loc[:, table_data.columns[:2]].round()
        table_data[table_data.columns[:2]] = table_data.loc[:, table_data.columns[:2]].astype(Int64Dtype())

        table_data = table_data.astype(object)
        table_data.index = table_data.index.map(
            lambda x: fold_text(normalize('NFKC', str(x)), length=37, max_length=1000, delimiter='--nl--'))

        table_data.reset_index(inplace=True)
        table_data.set_index(inplace=True, keys=['タイトル'])
        markdown_dict[key] = table_data.replace(NA, 'no data').to_markdown().replace('--nl--', '')
        if table_data.index.__len__() > 15:
            table_data = table_data.loc[table_data.index[:15], :]
        with open(join(getcwd(), 'html', key + '.html'), mode='w', encoding='utf-8') as f:
            f.write(html_base(name=filter(lambda x: x.db_key == key, playlists())[0].display_name,
                              content=table_data.to_html(render_links=True, notebook=True, justify='center')))
        run([firefox_path, '--screenshot', join(getcwd(), 'table', f'{key}.png'),
             f'http://127.0.0.1:8888/html/{key}.html', '--window-size=3000,3000'], stdout=stdout, stderr=stderr)
        crop(key)

    serve.terminate()
with open(file=join(getcwd(), 'markdown.pickle'), mode='wb') as f:
    dump(obj=markdown_dict, file=f)
