#!/usr/bin/env python
import os
from ritetag import RiteTagApi, read_env_file, get_env, ImageBuilder, AnimationType, FontList

read_env_file('.env')
access_token = get_env('ACCESS_TOKEN')

client = RiteTagApi(access_token)

ib = ImageBuilder('If you love life, don\'t waste time, for time is what life is made up of', 'Bruce Lee')
ib.animation(AnimationType.glint)\
    .quote_font(FontList.Lora)\
    .author_font(FontList.Lato_Black)

response = client.text_to_image(ib)
path = response.save(os.getcwd(), 'image_name')

print('Saved: {}'.format(path))
