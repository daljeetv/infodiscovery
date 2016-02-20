#/usr/bin/env python
# coding=utf-8


from django.http import HttpResponse
from django.utils import simplejson

def home(request):
    return HttpResponse("Hello, welcome to my home.")\

def results(request, website_id):
    response = "You are looking at the results for website: %s"
    json_stuff = simplejson.dumps({"list_of_jsonstuffs" : ["a", "b"]})
    return HttpResponse(json_stuff, content_type ="application/json")

    #return HttpResponse(response % website_id)
