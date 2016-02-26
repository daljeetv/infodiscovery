#/usr/bin/env python
# coding=utf-8


from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from websiteFinder import websiteFinder
from website import Website
from .forms import PostForm
from django.http import HttpResponseRedirect

def home(request):
    print request.method
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(form.cleaned_data['website'])
    else:
        form = PostForm()
    return render(request, 'infodiscovery/index.html',  {'form': form})

def results(request, website_id):
    websiteFinderInstance = websiteFinder(website_id)
    website = websiteFinderInstance.find_related()
    context = {'result_list' : website.alexaRanks, }
    return render(request, 'infodiscovery/results.html', context)
