import json
import os
import pprint
import numpy
import requests

FIELD = 'business_discovery.username({name}){{name,username,followers_count,media{{comments_count,like_count}}}}'

API_VER = '13.0'

ACCESS_TOKEN = os.environ['TOKEN']

API_ENDPOINT = 'https://graph.facebook.com'

MY_IG_ID = '17841405931345347'

request_url = API_ENDPOINT + '/v' + API_VER + '/' + MY_IG_ID + '?fields=' + \
              FIELD + '&access_token=' + ACCESS_TOKEN


def get_data(username=None):
    if username is None:
        return Exception
    return json.loads(requests.get(request_url.format(name=username)).text)


def process_data(data):
    display_name = data['business_discovery']['name']
    follower_count = data['business_discovery']['followers_count']
    comments_count_mean = numpy.mean([obj['comments_count'] for obj in data['business_discovery']['media']['data']])
    like_counts = [obj['like_count'] for obj in data['business_discovery']['media']['data'] if 'like_count' in obj]
    if not like_counts:
        like_count_mean = 0.0
    else:
        like_count_mean = numpy.mean(like_counts)
    return [display_name, follower_count, comments_count_mean, like_count_mean]


with open('instagram_user.list', 'r') as f:
    user_list = f.read().split()

pprint.pprint(user_list)

for user in user_list:
    if '#' in user:
        continue
    json_data = get_data(user)
    proceed_data = process_data(data=json_data)
    pprint.pprint(proceed_data)
