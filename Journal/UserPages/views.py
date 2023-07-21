from django.shortcuts import render
from django.http import HttpResponse
import random
from time import localtime, strftime

# Create your views here.

def index(request):
    homePageResponses = strftime("%a, %d %b %Y %H:%M:%S", localtime())
    return HttpResponse(f"Time is construct!<br>{homePageResponses}")
