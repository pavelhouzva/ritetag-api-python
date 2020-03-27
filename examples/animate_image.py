#!/usr/bin/env python
import os
from ritetag import RiteTagApi, read_env_file, get_env

read_env_file('.env')
access_token = get_env('ACCESS_TOKEN')

client = RiteTagApi(access_token)

result = client.animate_image('https://jpeg.org/images/jpeg-home.jpg')
path = result.save(os.getcwd(), 'animated_image')

print('Saved: {}'.format(path))
