#!/usr/bin/env python
from ritetag import RiteTagApi, read_env_file, get_env

read_env_file('.env')
access_token = get_env('ACCESS_TOKEN')

client = RiteTagApi(access_token)

result = client.extract_top_image_for_url('https://fedoramagazine.org/secure-ntp-with-nts/')

print(result)
