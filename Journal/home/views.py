from django.shortcuts import render
from django.http import HttpResponse
import random
from time import localtime, strftime

# Create your views here.

def index(request):
    homePageResponses = ["Sure Why Not on the homepage!", "You really thought this was working homepage", "Joke is on you this is under developement", strftime("%a, %d %b %Y %H:%M:%S", localtime())]
    return HttpResponse(homePageResponses[random.randint(0,3)])
