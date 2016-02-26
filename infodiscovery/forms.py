#!/usr/bin/env python
# coding=utf-8


from django import forms



#This is the name of our form. It is a ModelForm.
class PostForm(forms.Form):
    website = forms.CharField(label="website", max_length=100)

