from shutil import unpack_archive, rmtree
from urllib.request import urlretrieve
from os.path import join, exists
from os import getcwd, makedirs

if exists(join(getcwd(), 'fonts')):
    rmtree(join(getcwd(), 'fonts'))

makedirs(join(getcwd(), 'fonts'), exist_ok=True)
makedirs(join(getcwd(), 'fonts', 'emoji'), exist_ok=True)
makedirs(join(getcwd(), 'fonts', 'noto_sans_jp'), exist_ok=True)

urlretrieve('https://fonts.google.com/download?family=Noto%20Emoji', join(getcwd(), 'fonts', 'emoji.zip'))
urlretrieve('https://fonts.google.com/download?family=Noto%20Sans%20JP', join(getcwd(), 'fonts', 'noto_sans_jp.zip'))

unpack_archive(join(getcwd(), 'fonts', 'emoji.zip'), join(getcwd(), 'fonts', 'emoji'))
unpack_archive(join(getcwd(), 'fonts', 'noto_sans_jp.zip'), join(getcwd(), 'fonts', 'noto_sans_jp'))


def get_emoji_path() -> str:
    return join(getcwd(), 'fonts', 'emoji', 'static', 'NotoEmoji-Bold.ttf')


def get_sans_path() -> str:
    return join(getcwd(), 'fonts', 'noto_sans_jp', 'NotoSansJP-Regular.otf')
