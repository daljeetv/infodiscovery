#/usr/bin/env python
# coding=utf-8

import urllib
from lxml import etree
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import urllib
import socket
from urlparse import urlparse

class Website:

    def __init__(self, website, listOfWebsites):
        self.website = website

        #listOfRootWebsites is a dictionary (website, # of occurences)
        self.listOfRootWebsites = self.getListOfRootWebsites(listOfWebsites)

        #alexaRanks is a dictionary (website, alexa rank)
        self.alexaRanks = self.getAlexaRanks(self.listOfRootWebsites)

    def getListOfRootWebsites(self, listOfWebsites):
        dictionary = {}
        if listOfWebsites is None:
            return dictionary
        for website in listOfWebsites:
            website = self.getRoot(website)
            if(dictionary.get(website) is None):
                dictionary[website] = 1
            else:
                dictionary[website] = dictionary[website] + 1
        return dictionary

    def getRoot(self, website):
        o = urlparse(website)
        return o.netloc

    def getAlexaRanks(self, listOfWebsites):
        dictionary = {}
        if listOfWebsites is None:
            return dictionary
        for website in listOfWebsites:
            if(dictionary.get(website) is None):
                dictionary[website] = self.get_alexa_rank(website)
        return dictionary

    @staticmethod
    def get_alexa_rank(website):
        alexaWebpage = "http://www.alexa.com/siteinfo/" + website
        print alexaWebpage
        f = urllib.urlopen(alexaWebpage)
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        resultSet = soup.find_all("strong")
        if resultSet is None or len(resultSet) < 8:
            return -1
        alexaRankAsStr =  str(resultSet[8]).split("\n")[1].split(" ")[0]
        if "," in alexaRankAsStr:
            alexaRankAsStr = alexaRankAsStr.replace(",","")
        print alexaWebpage + " alexaRank: " + alexaRankAsStr
        return int(alexaRankAsStr)
