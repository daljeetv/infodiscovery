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
from website import Website
try:
    import cPickle as pickle
except:
    import pickle
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
        listOfWebsites = self.find_related_websites()
        websiteInstance = Website(self.website, listOfWebsites)
        return websiteInstance

    def find_related_websites(self):
        if(self.fileExists()):
            try:
                return self.findFileAndReturnContents()
            except:
                pass
        visited = set()
        links = self.findAllLinks(self.website)
        rootLinks = self.getAllCleanLinks(links)
        for rootWebsite in rootLinks:
            if rootWebsite not in visited:
                print "visiting: " + rootWebsite
                visited.add(rootWebsite)
                newLinks = self.findAllLinks(rootWebsite)
                newRootLinks = self.getAllCleanLinks(newLinks)
                for newRoot in newRootLinks:
                    if newRoot not in rootLinks:
                        rootLinks.append(newRoot)
        self.storeInFile(rootLinks)
        return rootLinks

    def fileExists(self):
        return os.path.isfile(self.getPickleFile())

    def findFileAndReturnContents(self):
        print "returning contents for file : " + self.getPickleFile()
        try:
            return pickle.load(open(self.getPickleFile(), 'r + b'))
        except:
            raise e

    def storeInFile(self, rootLinks):
        print self.getPickleFile()
        pickle.dump(rootLinks, open(self.getPickleFile(), 'wb'))

    def getPickleFile(self):
        if self.website[-1] == '/':
            self.website= self.website[:-1]
        websiteFileName = self.website + '.p'
        websiteFileName.encode('ascii','ignore')
        return websiteFileName

    def getAllCleanLinks(self,links):
        if links is None:
            return []
        links = set(links)
        rootLinks = []
        for link in links:
            print "Link before Cleaning: " + link
            if "http://www." in link:
                link = link.replace("http://wwww.", "www.")
            elif "https://www." in link:
                link = link.replace("https://www.", "www.")
            elif "http://" in link:
                link = link.replace("http://", "www.")
            elif "https://" in link:
                link = link.replace("https://", "www.")
            elif "//www." in link:
                link = link.replace("//www.", "www.")
            elif "www." in link:
                pass
            else:
                if len(link) > 0 and link[0] == '/':
                        link = link[1:]
                if(self.website[-1] == '/'):
                    link = self.website + link
                else:
                    link = self.website + "/"+ link

            if " \u200e" in link:
                link = link.replace(" \u200e","")
            print "New Clean Link: " + link
            rootLinks.append(link)
        if rootLinks is None:
            print "We found no clean links"
        else:
            print "We found " + str(len(rootLinks))  + " clean links"
        return rootLinks

    def findAllLinks(self, website):
        if(self.website not in website):
            print "This website does not come from primary website."
            return None
        url = self.SEARCH_URL.format(url_quote(website.encode('ascii','ignore')))
        try:
            response =self.get_response(url)
        except:
            return None
        links =  self.get_links_from_response(response)
        for link in links:
            logger.debug(link)
        links =  [x['href'] for x in links]
        if links is None:
            print "no new links found for website " + website
        else:
            print "we found " + str(len(links)) + "for website: " + website
        return links

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
