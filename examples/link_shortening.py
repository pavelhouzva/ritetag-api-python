#!/usr/bin/env python
from ritetag import RiteTagApi, read_env_file, get_env

read_env_file('.env')
access_token = get_env('ACCESS_TOKEN')

client = RiteTagApi(access_token)

ctas = client.list_of_cta()

link = client.shorten_url('https://twitter.com', ctas[0].id)

print('Original link: {}, Shorten link: {}'.format(link.original, link.url))
