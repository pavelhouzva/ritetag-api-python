import ritetag
import pytest
from unittest import TestCase


class TestBasics(TestCase):

    def setUp(self) -> None:
        access_token = ''
        self.client = ritetag.RiteTagApi(access_token)

    def test_sanitize_hashtag(self):
        assert self.client._sanitize_hashtag('#hello') == 'hello'
        assert self.client._sanitize_hashtag('#blob') == 'blob'

    def test_invalid_hashtag(self):
        with pytest.raises(ritetag.RiteTagException, match=r'Invalid hashtag'):
            self.client._sanitize_hashtag('#bl ob')

    def test_sanitize_domain(self):
        assert self.client._sanitize_domain('google.com') == 'google.com'
        assert self.client._sanitize_domain('https://google.com') == 'google.com'

    def test_invalid_domain_1(self):
        with pytest.raises(ritetag.RiteTagException, match=r'Invalid domain'):
            self.client._sanitize_domain('ritetag.com/test')

    def test_invalid_domain_2(self):
        with pytest.raises(ritetag.RiteTagException, match=r'Invalid domain'):
            self.client._sanitize_domain('ftp://ritetag.com')

    def test_sanitize_url(self):
        assert self.client._sanitize_url('google.com') == 'http://google.com'
        assert self.client._sanitize_url('https://google.com') == 'https://google.com'

    def test_invalid_url(self):
        with pytest.raises(ritetag.RiteTagException, match=r'Invalid url'):
            self.client._sanitize_url('ftp://ritetag.com')