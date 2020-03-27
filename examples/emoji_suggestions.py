#!/usr/bin/env python
from ritetag import RiteTagApi, read_env_file, get_env

read_env_file('.env')
access_token = get_env('ACCESS_TOKEN')

client = RiteTagApi(access_token)

result = client.emoji_suggestion('TIL the Austrian mathematician Kurt Godel had an obsessive fear of being poisoned,'
                                 ' and would only eat food prepared by his wife. When she had to be hospitalized'
                                 ' in 1977, he refused to eat at all and died weighing 65 pounds.')

print(', '.join(result))
