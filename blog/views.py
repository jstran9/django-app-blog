from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    # need request to get function to work later on.
    return HttpResponse('<h1>Blog Home</h1>')


def about(request):
    return HttpResponse('<h2>Blog About Roxy!</h2>')
