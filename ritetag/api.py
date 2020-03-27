import requests
import base64
import re

from .decorators import api_call, api_request
from .response import *
from .builders import *
from .exceptions import RiteTagException, ImageFormatException
try:
    # python2
    from urlparse import urlparse
except:
    # python3
    from urllib.parse import urlparse


class RiteTagApi:

    def __init__(self, client_id):
        self.base_uri = 'https://api.ritekit.com'
        self.client_id = client_id
        self.limit = None
        self.callbacks = []

    def _get_headers(self, json=False):
        headers = {
            'User-Agent': 'RiteTag API client 1.0',
            'Authorization': 'Bearer {}'.format(self.client_id)
        }
        if json:
            headers['Content-Type'] = 'application/json'
        return headers

    def _set_api_limits(self, headers: dict):
        keys = ['X-Rate-Limit-Limit', 'X-Rate-Limit-Used', 'X-Rate-Limit-Reset']
        exists = all([x in headers for x in keys])

        if exists:
            self.limit = Limit(
                headers[keys[0]],
                headers[keys[1]],
                headers[keys[2]],
            )
        else:
            raise RiteTagException('Something went wrong.')

    def _check_api_limits(self):
        for c in self.callbacks:
            if self.limit.usage >= c[0]:
                c[1](self.limit)

    def _sanitize_hashtag(self, hashtag: str) -> str:
        if hashtag is None:
            raise RiteTagException('Invalid hashtag.')
        hashtag = hashtag.strip().lstrip('#')
        if len(hashtag) == 0 or ' ' in hashtag:
            raise RiteTagException('Invalid hashtag.')
        return hashtag

    def _check_scheme(self, url: str) -> str:
        scheme_regex = r"^([a-z]+):\/\/"
        f = re.findall(scheme_regex, url)
        if len(f) > 0:
            if f[0] not in ['http', 'https']:
                raise RiteTagException('Invalid scheme')
        else:
            url = 'http://{}'.format(url)
        return url

    def _sanitize_domain(self, domain: str) -> str:
        try:
            domain = self._check_scheme(domain)
            result = urlparse(domain)
            if domain != '{}://{}'.format(result.scheme, result.netloc):
                raise RiteTagException('Invalid domain')
            return result.netloc
        except Exception as e:
            raise RiteTagException('Invalid domain')

    def _sanitize_url(self, url: str) -> str:
        try:
            url = self._check_scheme(url)
            result = urlparse(url)
            return result.geturl()
        except Exception as e:
            raise RiteTagException('Invalid url')

    def _get_image_from_url(self, url) -> Image:
        img = requests.request('GET', url, stream=True)
        return Parser.image(img, True)

    @api_request
    def _get_request(self, path: str, params: dict, stream: bool = False) -> Response:
        return requests.request('GET', '{}{}'.format(self.base_uri, path),
                                headers=self._get_headers(), params=params, stream=stream)

    @api_request
    def _post_request(self, path: str, data: dict, params: dict = {}, stream: bool = False) -> Response:
        resp = requests.request('POST', '{}{}'.format(self.base_uri, path,),
                                headers=self._get_headers(json=True), params=params, json=data, stream=stream)
        return resp

    @api_call
    def hashtag_stats(self, hashtags: [str]) -> [Hashtag]:
        hashtags = map(self._sanitize_hashtag, hashtags)
        response = self._get_request('/v1/stats/multiple-hashtags', {'tags': ','.join(hashtags)})
        return Parser.hashtag_list(response.json(), 'stats')

    @api_call
    def auto_hashtag(self, post: str, max_hashtags: int = 2,
                     hashtag_position: HashtagPosition = HashtagPosition.auto) -> str:
        response = self._get_request('/v1/stats/auto-hashtag',
                                     {'post': post, 'maxHashstags': max_hashtags, 'hashtagPosition': hashtag_position})
        return Parser.get_text(response.json(), 'post')

    @api_call
    def hashtag_suggestion_for_text(self, text: str) -> [Hashtag]:
        response = self._get_request('/v1/stats/hashtag-suggestions', {'text': text})
        return Parser.hashtag_list(response.json(), 'data')

    @api_call
    def hashtag_suggestion_for_image(self, image):
        try:
            with open(image, "rb") as f:
                result = base64.b64encode(f.read()).decode('utf-8')
        except IOError:
            result = self._sanitize_url(image)

        body = {
            'image': result
        }
        print(body)
        response = self._post_request('/v1/stats/hashtag-suggestions-image', body)

        print(response.request.body)
        print(response.content)
        return Parser.hashtag_list(response.json(), 'data')

    @api_call
    def history(self, hashtag) -> [HashtagHistory]:
        hashtag = self._sanitize_hashtag(hashtag)
        response = self._get_request('/v1/stats/history/{}'.format(hashtag), {})
        return Parser.history(response.json())

    @api_call
    def trending_hashtags(self, green: bool = True, latin: bool = True) -> [Hashtag]:
        response = self._get_request('/v1/search/trending', {'green': int(green), 'latin': int(latin)})
        return Parser.hashtag_list(response.json(), 'tags')

    @api_call
    def banned_instagram_hashtags(self, post: str) -> InstagramBannedHashtag:
        response = self._get_request('/v2/instagram/hashtags-cleaner', {'post': post})
        return Parser.banned_instagram_hashtags(response.json())

    @api_call
    def emoji_suggestion(self, text) -> [str]:
        response = self._get_request('/v1/emoji/suggestions', {'text': text})
        return Parser.emoji(response.json())

    @api_call
    def auto_emojify(self, text) -> str:
        response = self._get_request('/v1/emoji/auto-emojify', {'text': text})
        return Parser.get_text(response.json(), 'text')

    @api_call
    def text_to_image(self, image_builder: ImageBuilder):
        response = self._get_request('/v1/images/quote', params=image_builder.build())
        url = Parser.url_from_image(response.json())
        return self._get_image_from_url(url)

    @api_call
    def animate_image(self, url, animation_type: AnimationType = AnimationType.glint):
        response = self._get_request('/v1/images/animate', {'url': url, 'type': animation_type}, stream=True)
        return Parser.image(response)

    @api_call
    def company_logo(self, domain) -> Image:
        domain = self._sanitize_domain(domain)
        response = self._get_request('/v1/images/logo', {'domain': domain}, stream=True)
        # response.raw.decode_content = True
        return Parser.image(response)

    @api_call
    def list_of_cta(self) -> [Cta]:
        response = self._get_request('/v1/link/cta', {})
        return Parser.cta_list(response.json())

    @api_call
    def shorten_url(self, url: str, cta_id: int) -> Link:
        url = self._sanitize_url(url)
        response = self._get_request('/v1/link/short-link', {'url': url, 'cta': cta_id})
        return Parser.link(response.json())

    def on_limit(self, percentage: int, callback: callable):
        self.callbacks.append(
            [percentage, callback]
        )
