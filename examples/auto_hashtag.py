#!/usr/bin/env python
from ritetag import RiteTagApi, read_env_file, get_env, HashtagPosition

read_env_file('.env')
access_token = get_env('ACCESS_TOKEN')

client = RiteTagApi(access_token)

result = client.auto_hashtag('Is artificial intelligence the future of customer service?', 2, HashtagPosition.auto)

print(result)
