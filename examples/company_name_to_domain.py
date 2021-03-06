#!/usr/bin/env python
from ritetag import RiteTagApi, read_env_file, get_env

read_env_file('.env')
access_token = get_env('ACCESS_TOKEN')

client = RiteTagApi(access_token)

result = client.company_name_to_domain('Google')


def log(message):
    print(message)

[log(r) for r in result]
