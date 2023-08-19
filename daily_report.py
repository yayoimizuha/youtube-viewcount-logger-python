from os.path import join
from tweet import generate_txt
from sys import argv
from os import getcwd
from urllib.parse import quote
from pickle import load

with open(file=join(getcwd(), 'markdown.pickle'), mode='rb') as f:
    markdown_table_dict = load(file=f)

update_data = generate_txt()
release_note_md = str()
for key, value in update_data.items():
    print(key, flush=True)
    release_note_md += f'## {key}\n'
    release_note_md += value[0].split('\n', maxsplit=1)[1].replace('\n', '  \n') + '\n'
    release_note_md += f'  {markdown_table_dict[key]}  \n'
    release_note_md += (
        f'![{key}の再生回数の推移](https://raw.githubusercontent.com/yayoimizuha/youtube-viewcount-logger'
        f'-python/{argv[1]}/graph/{quote(key)}.png)\n  \n')

with open(file=join(getcwd(), 'daily_report.md'), mode='w', encoding='utf-8') as f:
    f.write(release_note_md)
