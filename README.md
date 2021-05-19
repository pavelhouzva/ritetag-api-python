# RiteTag API client

Python API client

## Documentation

[API Documentation](https://documenter.getpostman.com/view/2010712/SzS7Qku5?version=latest#3a6540d0-61e3-4333-b353-f1072621a23b)

## Installation

`pip install --user ritetag`


## Usage

### In The Code
```python
from ritetag import RiteTagApi

access_token = 'token'
client = RiteTagApi(access_token)

def limit_80_percentage_reached(limit):
    message = 'Used {}% of API credits. The limit resets on {}'.format(limit.usage, limit.reset)
    print(message)

# The callback function is triggered when 80% of the API limit is reached
client.on_limit(80, limit_80_percentage_reached)

stats = client.hashtag_stats(['jobs', 'hello'])

for data in stats:
    print('#{}: {} tweets per hour'.format(data.hashtag, data.tweets))

```

output:

```
#jobs: 642 tweets per hour
#hello: 25 tweets per hour
```

### In The Console

```
ritetag-api -h
usage: ritetag-api [-h] [-t ACCESS_TOKEN] [-m MAX_HASHTAGS] [-p {auto,end}]
                   [-f FILENAME] [-ci CTA_ID]
                   {hashtag_stats,auto_hashtags,hashtag_suggestions,hashtag_history,emojis_suggestion,auto_emojify,company_logo,list_of_cta,shorten_link}
                   [hashtags [hashtags ...]]

RiteTag API console client.

positional arguments:
  {hashtag_stats,auto_hashtags,hashtag_suggestions,hashtag_history,emojis_suggestion,auto_emojify,company_logo,list_of_cta,shorten_link}
                        action
  hashtags              hashtags

optional arguments:
  -h, --help            show this help message and exit
  -t ACCESS_TOKEN, --access_token ACCESS_TOKEN
                        access token
  -m MAX_HASHTAGS, --max_hashtags MAX_HASHTAGS
  -p {auto,end}, --hashtag_position {auto,end}
  -f FILENAME, --filename FILENAME
  -ci CTA_ID, --cta_id CTA_ID
```


```
export ACCESS_TOKEN={access_token}
ritetag-api hashtag_stats jobs hello
```

or

`ritetag-api -t {access_token} hashtag_stats jobs hello`

output:

```
Used 19.89% of API credits. The limit resets on 2020-04-01.
==== Stats of #jobs ====
tweets: 642
retweets: 62
exposure: 1984429
mentions: 9.03427%
links: 35.04673%
images: 35.04673%
color: HOT_NOW
media count: 3490073

==== Stats of #hello ====
tweets: 25
retweets: 4
exposure: 32567
mentions: 32.0%
links: 32.0%
images: 32.0%
color: HOT_NOW
media count: 18896544

```
### Company logo API (console)

##### Example 1 - google.com

```shell
# Company logo example
ritetag-api -t {token} company_logo google.com
```

```
Looking for logo - google.com
Used 0.14% of API credits. The limit resets on 2021-06-01.
Downloading logo - google.com
Image is saved google_com.svg - google.com
Downloading square logo - google.com
Image is saved google.com - google_com_square.png

```

##### Example 2 - notfound.test with Generate fallback

```shell
# Company logo example
ritetag-api -t {token} company_logo -g 1 company_logo notfound.test
```

```
Looking for logo - notfound.test
Used 0.14% of API credits. The limit resets on 2021-06-01.
Logo is generated.
Downloading logo - notfound.test
Image is saved notfound_test.png - notfound.test
Downloading square logo - notfound.test
Image is saved notfound.test - notfound_test_square.png

```

##### Example 3 -  notfound.test without Generate fallback

```shell
# Company logo example
ritetag-api -t {token} company_logo -g 0 company_logo notfound.test
```

```
Looking for logo - notfound.test
Used 0.14% of API credits. The limit resets on 2021-06-01.
Downloading logo - notfound.test
Error Logo not found - notfound.test
Downloading square logo - notfound.test
Error Logo not found - notfound.test
```