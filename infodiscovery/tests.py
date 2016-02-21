#!/usr/bin/env python
# coding=utf-8


from websiteFinder import websiteFinder

websiteFinderInstance = websiteFinder("www.gwern.net")
websites = websiteFinderInstance.find_related()
for website in websites:
    print website
