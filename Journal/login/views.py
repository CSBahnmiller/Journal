from django.shortcuts import render
from django.http import HttpResponse
import random
from time import localtime, strftime

# Create your views here.

def index(request):
    return HttpResponse(f'{strftime("%a, %d %b %Y %H:%M:%S", localtime())} <br> Landing page for login.')
