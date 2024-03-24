import json
from asyncio import run
from os import getenv, getcwd
from os.path import join
from sqlite3 import connect
from urllib.parse import urlencode
from const import pack_comma
import requests
from aiohttp import ClientSession
from google import generativeai
from google.generativeai import GenerationConfig
from google.generativeai.types import HarmCategory, HarmBlockThreshold

GEMINI_API_KEY = getenv('GEMINI_API_KEY', default='')
if GEMINI_API_KEY == '':
    print('No Gemini API Key.')
    exit(-1)

generativeai.configure(api_key=GEMINI_API_KEY)

# Set up the model
generation_config = GenerationConfig(
    temperature=0.0,
    top_p=1.0,
    top_k=1,
    max_output_tokens=1024
)

safety_settings = [
    {
        "category": HarmCategory.HARM_CATEGORY_HARASSMENT,
        "threshold": HarmBlockThreshold.BLOCK_NONE
    },
    {
        "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        "threshold": HarmBlockThreshold.BLOCK_NONE
    },
    {
        "category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        "threshold": HarmBlockThreshold.BLOCK_NONE
    },
    {
        "category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        "threshold": HarmBlockThreshold.BLOCK_NONE
    },
]

model = generativeai.GenerativeModel(model_name="gemini-1.0-pro-001",
                                     generation_config=generation_config,
                                     safety_settings=safety_settings)


async def trim_title_with_ai(string: str, cache: dict) -> str:
    if string in cache:
        json_data = cache[string]
    else:
        prompt_parts = ["""以下にYouTubeタイトルが与えられるので、YouTubeタイトルから楽曲名と歌手、バージョン、エディションをJSON形式で{"song_name":"XXXXX","singer":["AAAAA","BBBB"],"edition":"CCCCC","version":"DDDDD"}というフォーマットで出力しなさい。Markdownのコードブロックは使わないこと。
楽曲名は、以下のルールに従って加工しなさい。
・それぞれの項目に関する文字列がなかった場合、空白にすること。
・楽曲名の読み仮名は、楽曲名から除きなさい。
・英訳があった場合は楽曲名に含めてはいけない。
・バージョン(例:Ver.やversionやver等)に関する文字列があった場合、それをバージョンに含めなさい。
・バージョンに関する文字列がなかった場合、バージョンは空文字とすること。
・エディションや動画に関する文字列があった場合それをエディションに含めなさい。
・Promotion EditやMVやMusic Videoなどの単語があった場合、エディションは空文字にしなさい。
・エディションや動画に関する文字列がなかった場合、エディションは空文字とすること。
    
    
    
""" + string]
        response = await model.generate_content_async(prompt_parts)
        json_data: dict = json.loads(response.text)
        print("Generating title by Gemini ..." + response.text)
        cache[string] = json_data
        # with open(join(getcwd(), "gemini-cache.json"), mode="w", encoding="utf-8") as f:
        #     f.truncate(0)
        #     f.write(json.dumps(gemini_cache, indent=2, ensure_ascii=False))
    return_text = json_data['song_name']
    if json_data['singer']:
        return_text += (' : ' + ','.join(json_data['singer']))
    if json_data['edition'] != '':
        return_text += (' - ' + json_data['edition'])
    if json_data['version'] != '':
        return_text += (' - ' + json_data['version'])
    return return_text


if __name__ == '__main__':
    with open(join(getcwd(), "gemini-cache.json"), mode="r", encoding="utf-8") as f:
        gemini_cache = json.loads(f.read())
    sess = ClientSession(trust_env=True)
    connector = connect("save.sqlite")
    cursor = connector.cursor()
    table_name = [name[0] for name in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
    urls: set[str] = set()
    for name in table_name:
        urls |= {url[0] for url in cursor.execute(f"SELECT \"index\" FROM {pack_comma(name)}").fetchall()}
    for url in urls:
        api_res = requests.get(
            "https://www.googleapis.com/youtube/v3/videos?" + urlencode(
                {'part': 'statistics,snippet', 'fields': 'items/snippet/title',
                 'id': url.removeprefix('https://youtu.be/'), 'key': getenv('YTV3_API_KEY')})).json()
        print(url.removeprefix('https://youtu.be/'))
        # print(api_res)
        try:
            title = api_res['items'][0]['snippet']['title']
        except BaseException as e:
            print(api_res)
            continue
        print(title)
        print("structured title: " + run(trim_title_with_ai(title, gemini_cache)))
    print(len(urls))

    run(sess.close())
    with open(join(getcwd(), "gemini-cache.json"), mode="r", encoding="utf-8") as f:
        f.write(json.dumps(gemini_cache, indent=2, ensure_ascii=False))
