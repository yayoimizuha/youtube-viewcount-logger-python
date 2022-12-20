import aiohttp
import asyncio
from os import getenv
from urllib import parse

YTV3_ENDPOINT = "https://www.googleapis.com"

API_KEY = getenv('YTV3_API_KEY', default='')
if API_KEY == '':
    print('No API Key.')
    exit(-1)


def query_builder(resource_type: str,
                  arg: dict,
                  content_id: str,
                  part: str,
                  service_name: str = "youtube",
                  version: str = "v3",
                  key: str = API_KEY) -> str:
    base_url: str = "/".join([YTV3_ENDPOINT, service_name, version, resource_type])


print(query_builder(arg={"a": 1}, content_id="b", part="c", resource_type="d"))
