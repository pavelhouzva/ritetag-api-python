#!/usr/bin/env python
import os
from ritetag import RiteTagApi, read_env_file, get_env

read_env_file('.env')
access_token = get_env('ACCESS_TOKEN')

client = RiteTagApi(access_token)

result = client.company_logo('google.com')

print('Url: {}'.format(result))
