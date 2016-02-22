#!/usr/bin/env python
# coding=utf-8


from websiteFinder import websiteFinder
from website import Website


def test_find_related():
    websiteFinderInstance = websiteFinder("www.gwern.net")
    websites = websiteFinderInstance.find_related()
    for website in websites:
        print website

def test_get_alexa_rank(website):
    websiteInstance = Website("www.gwern.net", None)
    print websiteInstance.get_alexa_rank("www.gwern.net")
    print websiteInstance.get_alexa_rank("www.a16z.com")
    print websiteInstance.get_alexa_rank("www.lesswrong.com")
    print websiteInstance.get_alexa_rank("www.facebook.com")
    print websiteInstance.get_alexa_rank("www.amazon.com")
#test_find_related()



website = "www.gwern.net"
test_get_alexa_rank(website)
