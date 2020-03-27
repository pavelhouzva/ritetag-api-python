#!/usr/bin/env python
from ritetag import RiteTagApi, read_env_file, get_env

read_env_file('.env')
access_token = get_env('ACCESS_TOKEN')

client = RiteTagApi(access_token)

result = client.banned_instagram_hashtags('#instaphotography #instabeauty #instagirls #girlsofinstagram'
                                          ' #instanature #instagirl #photography #beauty #girls #nature #girl'
                                          ' #sky #water #balls #lady #ladies #woman #women #photograph #photographs'
                                          ' #beauties #sunlight #sitting #waters #skies #sit #photographies')

print('post without banned hashtags:')
print(result.post)

print('\nbanned hashtags:')
for banned in result.banned_hashtags:
    print(banned)
