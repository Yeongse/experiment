from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings

from .models import Subject, Choice, Player

import datetime
# Create your views here.

now = datetime.datetime.now()
pairs = [
    [3, 6], 
    [2, 1], 
    [1, 3], 
    [4, 2], 
    [5, 6], 
    [1, 4], 
    [5, 2], 
    [2, 3],
    [1, 6], 
    [5, 1], 
    [2, 6], 
    [4, 5],
    [3, 4],
    [5, 3], 
    [4, 6]
    ]

def index(request):
    return HttpResponse("index")

def task(request):
    return HttpResponse("task")

def interval(request):
    return HttpResponse("interval")