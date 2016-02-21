#/usr/bin/env python
# coding=utf-8



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
        return 1



