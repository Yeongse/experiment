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
values = {
    "avg": [0.216+(0.02*i) for i in range(50)],
    "hr": [i for i in range(50)], 
    "sb": [i for i in range(50)], 
    "defense": [35.3+(0.6*i) for i in range(50)], 
    "rbi": [2+(2*i) for i in range(50)], 
    "bb": [31+i for i in range(50)], 
    "risp": [0.162+(0.04*i) for i in range(50)], 
    "dp": [1+i for i in range(50)], 
    "disabled": [5.2+(0.4*i) for i in range(50)], 
    "age": [18.5+(0.5*i) for i in range(50)]
}

def index(request):
    return HttpResponse(values)

def task(request):
    return HttpResponse("task")

def interval(request):
    return HttpResponse("interval")

def make(request):
    import random
    if request.method == "POST":
        random_numbers = []
        return HttpResponseRedirect(reverse("choice:index"))
    return render(request, "choice/make.html", {})


# def book(request, flight_id):
#     if request.method == "POST":
#         flight = Flight.objects.get(pk=flight_id)
#         passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
#         print(passenger.flights)
#         passenger.flights.add(flight)
#         return HttpResponseRedirect(reverse("flights:flight", args=[flight_id]))