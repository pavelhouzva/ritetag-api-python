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
        # type: (str) -> RiteTagApi
        self.base_uri = 'https://api.ritekit.com'
        self.client_id = client_id
        self.limit = None
        self.callbacks = []

    def _get_headers(self, json=False):
        # type (bool) -> dict
        headers = {
            'User-Agent': 'RiteTag API client 1.0',
            'Authorization': 'Bearer {}'.format(self.client_id)
        }
        if json:
            headers['Content-Type'] = 'application/json'
        return headers

    def _set_api_limits(self, code, headers):
        # type: (int, dict) -> None
        if code == 401:
            raise RiteTagException('Invalid or expired token')

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

    def _sanitize_hashtag(self, hashtag):
        # type: (str) -> str
        if hashtag is None:
            raise RiteTagException('Invalid hashtag.')
        hashtag = hashtag.strip().lstrip('#')
        if len(hashtag) == 0 or ' ' in hashtag:
            raise RiteTagException('Invalid hashtag.')
        return hashtag

    def _check_scheme(self, url):
        # type: (str) -> str
        scheme_regex = r"^([a-z]+):\/\/"
        f = re.findall(scheme_regex, url)
        if len(f) > 0:
            if f[0] not in ['http', 'https']:
                raise RiteTagException('Invalid scheme')
        else:
            url = 'http://{}'.format(url)
        return url

    def _sanitize_domain(self, domain):
        # type: (str) -> str
        try:
            domain = self._check_scheme(domain)
            result = urlparse(domain)
            if domain != '{}://{}'.format(result.scheme, result.netloc):
                raise RiteTagException('Invalid domain')
            return result.netloc
        except Exception as e:
            raise RiteTagException('Invalid domain')

    def _sanitize_url(self, url):
        # type: (str) -> str
        try:
            url = self._check_scheme(url)
            result = urlparse(url)
            return result.geturl()
        except Exception as e:
            raise RiteTagException('Invalid url')

    def _get_image_from_url(self, url):
        # type: (str) -> Image
        img = requests.request('GET', url, stream=True)
        return Parser.image(img, True)

    @api_request
    def _get_request(self, path, params, stream=False):
        # type: (str, dict, bool) -> Response
        return requests.request('GET', '{}{}'.format(self.base_uri, path),
                                headers=self._get_headers(), params=params, stream=stream)

    @api_request
    def _post_request(self, path, data, params=None, stream=False):
        # type: (str, dict, dict, bool) -> Response
        if params is None:
            params = {}
        resp = requests.request('POST', '{}{}'.format(self.base_uri, path,),
                                headers=self._get_headers(json=True), params=params, json=data, stream=stream)
        return resp

    @api_call
    def hashtag_stats(self, hashtags):
        # type: ([str]) -> [Hashtag]
        """
        Returns real-time stats for up to 100 hashtags. Stats are updated hourly.

        Parameters
        ----------
        hashtags : [str]
             List of hashtag(s) without # mark
        """
        hashtags = map(self._sanitize_hashtag, hashtags)
        response = self._get_request('/v1/stats/multiple-hashtags', {'tags': ','.join(hashtags)})
        return Parser.hashtag_list(response.json(), 'stats')

    @api_call
    def auto_hashtag(self, post, max_hashtags=2,
                     hashtag_position=HashtagPosition.auto):
        # type: (str, int, HashtagPosition) -> str
        """
        Returns auto-hashtagged text of the post.

        Parameters
        ----------
        post : str
            Text up to 1000 characters into which hashtags should be added.
        max_hashtags: int
            Maximum number of hashtags to be added to the text
        hashtag_position: HashtagPosition
            Position of hashtags: end => at the end of the text, auto => anywhere in the text or at the end
        """
        response = self._get_request('/v1/stats/auto-hashtag',
                                     {'post': post, 'maxHashstags': max_hashtags, 'hashtagPosition': hashtag_position})
        return Parser.get_text(response.json(), 'post')

    @api_call
    def hashtag_suggestion_for_text(self, text):
        # type: (str) -> [Hashtag]
        """
        Returns list of hashtag suggestions for a single-word topic or for short block of text (up to 1000 characters).

        Parameters
        ----------
        text : str
            Text up to 1000 characters for which hashtags should be suggested
         """
        response = self._get_request('/v1/stats/hashtag-suggestions', {'text': text})
        return Parser.hashtag_list(response.json(), 'data')

    @api_call
    def hashtag_suggestion_for_image(self, image):
        # type: (str) -> [Hashtag]
        """
        Returns list of hashtag suggestions for an image. Takes into account both semantic
        relevancy as well as real-time hashtag engagement.

        Parameters
        ----------
        image : str
            URL of an image
        """
        try:
            with open(image, "rb") as f:
                result = base64.b64encode(f.read()).decode('utf-8')
        except IOError:
            result = self._sanitize_url(image)

        body = {
            'image': result
        }
        response = self._post_request('/v1/stats/hashtag-suggestions-image', body)
        return Parser.hashtag_list(response.json(), 'data')

    @api_call
    def history(self, hashtag):
        # type: (str) -> [HashtagHistory]
        """
        Returns historical stats for a given hashtag from the last 30 days.
        Add hashtag without hash mark to the URL.

        Parameters
        ----------
        hashtag : str
            Hashtag without # mark
        """
        hashtag = self._sanitize_hashtag(hashtag)
        response = self._get_request('/v1/stats/history/{}'.format(hashtag), {})
        return Parser.history(response.json())

    @api_call
    def trending_hashtags(self, green=True, latin=True):
        # type: (bool, bool) -> [Hashtag]
        """
        Returns list of hashtags currently trending on Twitter.

        Parameters
        ----------
        green : bool
            restrict results only to green hashtags (hot now).
        latin : bool
            restrict results only to hashtags with latin characters
        """
        response = self._get_request('/v1/search/trending', {'green': int(green), 'latin': int(latin)})
        return Parser.hashtag_list(response.json(), 'tags')

    @api_call
    def banned_instagram_hashtags(self, post):
        # type: (str) -> InstagramBannedHashtag
        """
        Detects and removes hashtags banned on Instagram from a list of hashtags.

        Parameters
        ----------
        post : str
            Text up to 1000 characters from which hashtags banned on Instagram should be removed.
        """
        response = self._get_request('/v2/instagram/hashtags-cleaner', {'post': post})
        return Parser.banned_instagram_hashtags(response.json())

    @api_call
    def emoji_suggestion(self, text):
        # type: (str) -> [str]
        """
        Returns list of emoji suggestions for a short block of text (up to 1000 characters).

        Parameters
        ----------
        text : str
            Text up to 1000 characters for which emojis should be suggested.
        """
        response = self._get_request('/v1/emoji/suggestions', {'text': text})
        return Parser.emoji(response.json())

    @api_call
    def auto_emojify(self, text):
        # type : (str) -> str
        """
        Returns text of the post with emoji added

        Parameters
        ----------
        text: str
            Text up to 1000 characters into which emojis should be added.
        """
        response = self._get_request('/v1/emoji/auto-emojify', {'text': text})
        return Parser.get_text(response.json(), 'text')

    @api_call
    def text_to_image(self, image_builder):
        # type: (ImageBuilder) -> Image
        """
        Returns an image created from text according to given style parameters

        Parameters
        ----------
        image_builder : ImageBuilder
            see ImageBuilder
        """
        response = self._get_request('/v2/image/quote', params=image_builder.build(), stream=True)
        return Parser.image(response)

    @api_call
    def animate_image(self, url, animation_type=AnimationType.glint):
        # type: (str, AnimationType) -> Image
        """
        Returns an animated GIF.

        Parameters
        ----------
        url : str
            URL of the original image
        animation_type : AnimationType
            Only "glint" is currently supported.
        """
        response = self._get_request('/v1/images/animate', {'url': url, 'type': animation_type}, stream=True)
        return Parser.image(response)

    @api_call
    def company_logo(self, domain, generateFallbackLogo=False):
        # type: (str, bool) -> str
        """
        Deprecated

        Returns a company logo based on website domain.
        If the logo is not in our database yet, it will be extracted from the site on the fly.
        White logo background is automatically removed to make the logo look better on color backgrounds.
        Note: It is not possible to access our company logo API publicly without authentication.
        If you wish to do so, you have to create a proxy on your own server that calls our API
        from the server side.

        Parameters
        ----------
        domain : str
            Hostname without http://
        generateFallbackLogo : bool
        """
        domain = self._sanitize_domain(domain)
        gen = 1 if generateFallbackLogo else 0
        response = self._get_request('/v2/company-insights/logo', {'domain': domain, 'generateFallbackLogo': gen})
        return Parser.company_logo(response.json())

    @api_call
    def company_logo_2(self, domain, generateFallbackLogo=False):
        # type: (str, bool) -> Logo
        """
        Returns a company logo based on website domain.
        If the logo is not in our database yet, it will be extracted from the site on the fly.
        White logo background is automatically removed to make the logo look better on color backgrounds.
        Note: It is not possible to access our company logo API publicly without authentication.
        If you wish to do so, you have to create a proxy on your own server that calls our API
        from the server side.

        Parameters
        ----------
        domain : str
            Hostname without http://
        generateFallbackLogo : bool
        """
        domain = self._sanitize_domain(domain)
        gen = 1 if generateFallbackLogo else 0
        response = self._get_request('/v2/company-insights/logo', {'domain': domain, 'generateFallbackLogo': gen})
        return Parser.company_logo_2(response.json())

    @api_call
    def list_of_cta(self):
        # type: () -> [Cta]
        """
        Returns list of available Link Ads for any given Rite.ly user.
        Requires each user to authenticate with RiteKit.
        """
        response = self._get_request('/v1/link/cta', {})
        return Parser.cta_list(response.json())

    @api_call
    def shorten_url(self, url, cta_id):
        # type: (str, int) -> Link
        """
        Returns a short link with a given Link Ad (a Rite.ly user's advertisements that are iFramed on URLs).

        Parameters
        ----------
        url : str
            URL to be shortened
        cta_id : int
            Link Ad ID returned by List of CTAs endpoint
        """
        url = self._sanitize_url(url)
        response = self._get_request('/v1/link/short-link', {'url': url, 'cta': cta_id})
        return Parser.link(response.json())

    def free_mail_detection(self, domain):
        # type: (str) -> bool
        """
        Returns true for a recognized free email address or domain.

        Filter out free personal emails (gmail.com, outlook.com) with freemail detection API; forward hot business
        leads to your sales team. Give special treatment only to those who register with business email addresses.
        Use this endpoint before calling Brand Colors and Company Logo so you spend credits on calls only for
        real leads.

        Parameters
        ----------
        domain : str
            domain or email address
        """
        domain = self._sanitize_domain(domain)
        response = self._get_request('/v2/person-insights/freemail-detection', {'domain': domain})
        return Parser.free_mail_detection(response.json())

    def disposable_email_detection(self, email):
        # type: (str) -> bool
        """
        Returns true for a recognized disposable email address

        Tired of free riders signing up with fake email addresses and using your app's free trial repeatedly?
        Stop wasting money for API calls, emails and other costs incurred by users who will never pay for anything.
        Prevent them from signing up with our Disposable Email Detection API.

        Parameters
        ----------
        email : str
            domain or email address
        """
        email = self._sanitize_domain(email)
        response = self._get_request('/v2/person-insights/disposable-email-detection', {'email': email})
        return Parser.disposable_email_detection(response.json())

    def email_typo(self, email):
        # type: (str) -> [str]
        """
        Returns an array of most likely corrected email domains.

        Users who make a typo in their email address never get your onboarding emails, cannot reset their password and
        cannot be even reached by your customer support. They are practically lost. With our Email Typo API you can
        check for typical mistakes in email addresses and show "Did you mean" suggestions right in your sign up form.

        Parameters
        ----------
        email : str
            domain or email address
        """
        email = self._sanitize_domain(email)
        response = self._get_request('/v2/person-insights/email-typo', {'email': email})
        return Parser.email_typo(response.json())

    def name_from_email_address(self, email):
        # type: (str) -> str
        """
        Returns name and surname derived from an email address.

        The less fields in a sign up form, the higher the completion rate. Asking for a real name of a user is seen as
        a nuisance serving no value for the user himself. However, using customer name in the UI or in the emails
        significantly improves conversion rates, open rates and even deliverability as it is an indication for spam
        filters that the email is probably personal. With Name from Email Address API, you can derive real names from
        email addresses without actually bothering users with filling unnecessary fields.

        Parameters
        ----------
        email : str
            domain or email address
        """
        email = self._sanitize_domain(email)
        response = self._get_request('/v2/person-insights/name-from-email-address', {'email': email})
        return Parser.name_from_email_address(response.json())

    def company_name_to_domain(self, name):
        # type: (str) -> [str]
        """
        Returns an array of most probable domains for a given company name.

        Use this API call to retrieve company domain that can be used in other RiteKit API calls, eg. Company Logo.

        Parameters
        ----------
        name : str
            company name
        """
        response = self._get_request('/v2/company-insights/name-to-domain', {'name': name})
        return response.json()['data']

    def brand_colors(self, domain):
        # type: (str) -> [str]
        """
        Returns array of brand colors for a given domain.

        Parameters
        ----------
        domain : str
            company name
        """
        domain = self._sanitize_domain(domain)
        response = self._get_request('/v2/company-insights/brand-colors', {'name': domain})
        return response.json()['data']

    def extract_hastags_for_url(self, url):
        # type: (str) -> [Hashtag]
        """
        Returns list of hashtag suggestions for any URL. Takes into account both semantic relevancy and
        real-time hashtag popularity.

        Parameters
        ----------
        url : str
            url
        """
        url = self._sanitize_url(url)
        response = self._get_request('/v2/stats/hashtags-for-url', {'url': url})
        return Parser.hashtag_list(response.json(), 'hashtags')

    def extract_article_for_url(self, url):
        # type: (str) -> ArticleForUrl
        """
        Returns a title and a text of an article extracted from a URL (ignoring text in headers, footers, columns etc.).
        Works in Arabic, Russian, Dutch, German, English, Spanish, French, Hebrew, Italian, Korean, Norwegian, Persian,
        Polish, Portuguese, Swedish, Hungarian, Finnish, Danish, Chinese, Indonesian, Vietnamese, Swahili, Turkish,
        Greek, Ukrainian.

        Parameters
        ----------
        url : str
            url
        """
        url = self._sanitize_url(url)
        response = self._get_request('/v2/text/extract-article', {'url': url})
        return Parser.article_for_url(response.json())

    def extract_top_image_for_url(self, url):
        # type: (str) -> str
        """
        Returns an image URL extracted from a page URL

        Parameters
        ----------
        url : str
            url
        """
        url = self._sanitize_url(url)
        response = self._get_request('/v2/image/extract-image', {'url': url})
        return response.json()['top_image']

    def on_limit(self, percentage, callback):
        # type: (int, callable) -> None
        self.callbacks.append(
            [percentage, callback]
        )
