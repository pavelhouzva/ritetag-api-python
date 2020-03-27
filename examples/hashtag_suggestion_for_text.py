#!/usr/bin/env python
from ritetag import RiteTagApi, read_env_file, get_env

read_env_file('.env')
access_token = get_env('ACCESS_TOKEN')

client = RiteTagApi(access_token)

result = client.hashtag_suggestion_for_text('When you give Alaskans a universal basic income, they still keep working.')


def log(message):
    print(message)

[log(hashtag) for hashtag in result]
