#!/usr/bin/env python
# coding=utf-8

import os
import requests
import logging
import random
from requests.exceptions import ConnectionError
from requests.exceptions import SSLError
from bs4 import BeautifulSoup
import random
import re
import sys
try:
    from urllib import getproxies
except ImportError:
    from urllib.request import get_proxies

try:
    from urllib.parse import quote as url_quote
except ImportError:
    from urllib import quote as url_quote

logger = logging.getLogger(__name__)

class websiteFinder:
    def __init__(self, website):
        self.SEARCH_URL = 'http://{0}'
        self.website = website
        self.prefixes = ["www."]
        self.URL = os.getenv('CITATION_MACHINE_URL') or 'lesswrong.com'

        self.USER_AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
                       'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
                       'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',
                       'Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',)

    def find_related(self):
        url = self.SEARCH_URL.format(url_quote(self.website))
        try:
            response =self.get_response(url)
        except:
            return {"Sorry, no links found"}
        links =  self.get_links_from_response(response)
        for link in links:
            logger.debug(link)
        return [x['href'] for x in links]
    def get_response(self,url):
            try:
                cleanUrl = self.cleanLink(url)
                return requests.get(cleanUrl, headers={'User-Agent': random.choice(self.USER_AGENTS)}, proxies=self.get_proxies(), verify=False)
            except requests.exceptions.SSLError as e:
                raise e

    def cleanLink(self,url):
        contained = [x for x in self.prefixes if x in url]
        for prefix in contained:
            url = url.replace(prefix, "")
            return url

    def get_links_from_response(self,resp):
        encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
        soup = BeautifulSoup(resp.content, from_encoding=encoding)
        return soup.find_all('a', href=True)

    def get_proxies(self):
        proxies = getproxies()
        filtered_proxies = {}
        for key, value in proxies.items():
            if key.startswith('http'):
                if not value.startswith('http'):
                    filtered_proxies[key] = 'http://%s' % value
                else:
                    filtered_proxies[key] = value
        return filtered_proxies