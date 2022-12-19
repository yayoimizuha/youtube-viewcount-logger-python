from googleapiclient.discovery import build
from concurrent.futures import ThreadPoolExecutor
from os import getenv, getcwd, path, environ
from const import playlists

API_KEY = getenv('YTV3_API_KEY', default='')

if API_KEY == '':
    print('No API Key.')
    exit(-1)
youtube = build(
    'youtube',
    'v3',
    developerKey=API_KEY
)

print(playlists())
