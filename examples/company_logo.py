#!/usr/bin/env python
import os
from ritetag import RiteTagApi, read_env_file, get_env

read_env_file('.env')
access_token = get_env('ACCESS_TOKEN')

client = RiteTagApi(access_token)

domains = ['google.com', 'masumaki.com']

for domain in domains:
    print('Domain: {}'.format(domain))
    result = client.company_logo_2(domain, True)
    print('Is found: {}'.format(result.is_found))
    if result.is_found:
        print('Is generated: {}'.format(result.is_generated))
        print('Original URL: {}'.format(result.logo()))
        print('Original URL (permanent): {}'.format(result.square_logo(True)))
        print('Square URL: {}'.format(result.logo()))
        print('Square URL (permanent): {}'.format(result.square_logo(True)))
        print('')
