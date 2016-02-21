#/usr/bin/env python
# coding=utf-8


from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from websiteFinder import websiteFinder


def home(request):
    return HttpResponse("Hello, welcome to my home.")\

def results(request, website_id):
    websiteFinderInstance = websiteFinder(website_id)
    websites = websiteFinderInstance.find_related()
    context = {'result_list' : websites, }
    return render(request, 'infodiscovery/results.html', context)

