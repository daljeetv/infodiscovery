#/usr/bin/env python
# coding=utf-8

import urllib
from lxml import etree
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup

class Website:

    def __init__(self, website, listOfWebsites):
        self.website = website

        #listOfRootWebsites is a dictionary (website, # of occurences)
        self.listOfRootWebsites = self.getListOfRootWebsites(listOfWebsites)

        #alexaRanks is a dictionary (website, alexa rank)
        self.alexaRanks = self.getAlexaRanks(listOfWebsites)

    def getListOfRootWebsites(self, listOfWebsites):
        dictionary = {}
        if listOfWebsites is None:
            return dictionary
        for website in listOfWebsites:
            if(dictionary.get(website) is None):
                dictionary[website] = 1
            else:
                dictionary[website] = dictionary[website] + 1
        return dictionary


    def getAlexaRanks(self, listOfWebsites):
        dictionary = {}
        if listOfWebsites is None:
            return dictionary
        for website in listOfWebsites:
            if(dictionary.get(website) is None):
                dictionary[website] = get_alexa_rank(website)
        return dictionary

    @staticmethod
    def get_alexa_rank(website):
        alexaWebpage = "http://www.alexa.com/siteinfo/" + website
        print alexaWebpage
        d = pq(alexaWebpage)
        #strong =  d('*[@id="traffic-rank-content"] > div > span > div > span > span > div')
        soup = BeautifulSoup(d.text(), 'html.parser')
        return soup.prettify().split("Updated Daily ")[1].split(" ")[0]
