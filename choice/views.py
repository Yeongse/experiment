from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings

from .models import Subject, Choice, Player, Weight

import datetime
# Create your views here.

now = datetime.datetime.now()
pairs = [
    [2, 5], 
    [1, 0], 
    [0, 2], 
    [1, 3], 
    [4, 5], 
    [0, 3], 
    [1, 4], 
    [1, 2],
    [0, 5], 
    [4, 0], 
    [1, 5], 
    [3, 4],
    [2, 3],
    [4, 2], 
    [3, 5]
]
values = {
    "avg": [round(0.216+(0.002*i), 3) for i in range(50)],
    "hr": [i for i in range(50)], 
    "sb": [i for i in range(50)], 
    "defense": [round(35.3+(0.6*i), 1) for i in range(50)], 
    "rbi": [2+(2*i) for i in range(50)], 
    "bb": [31+i for i in range(50)], 
    "risp": [round(0.162+(0.004*i), 3) for i in range(50)], 
    "dp": [1+i for i in range(50)], 
    "disabled": [round(5.2+(0.4*i), 1) for i in range(50)], 
    "age": [round(18.5+(0.5*i), 1) for i in range(50)]
}

# question_index: 0~59
def get_situation_index(_question_index):
    import math
    situation_index = math.floor(_question_index/15)
    return situation_index

# calc weight using geometrix mean, for AHP
def get_evaluate_matrix(_choice_array, _score_array):
    import numpy as np
    element_num = len(_choice_array)+1
    evaluate_matrix = np.eye(element_num)
    for i in range(element_num-1):
        for j in range(element_num-1-i):
            if _choice_array[i][j] == 1:
                evaluate_matrix[i][j+1+i] = _score_array[i][j]
                evaluate_matrix[j+1+i][i] = 1/_score_array[i][j]
            elif _choice_array[i][j] == -1:
                evaluate_matrix[i][j+1+i] = 1/_score_array[i][j]
                evaluate_matrix[j+1+i][i] = _score_array[i][j]
    return evaluate_matrix

def get_weight(_evaluate_matrix):
    from scipy.stats.mstats import gmean
    element_num = len(_evaluate_matrix)
    gmeans = [gmean(_evaluate_matrix[i]) for i in range(element_num)]
    gmean_sum = sum(gmeans)
    weights = [gmeans[i]/gmean_sum for i in range(element_num)]
    return weights

# register subject's name
def index(request):
    if request.method =="POST":
        subject_name = request.POST["name"]
        subject = Subject(name=subject_name)
        subject.save()
        request.session["name"] = subject_name
        return HttpResponseRedirect(reverse("choice:description1"))
    
    return render(request, "choice/index.html", {})

# description for choice and compare
def description1(request):
    return render(request, "choice/description1.html", {})
def description2(request):
    return render(request, "choice/description2.html", {})

# main function
def task(request, question_index):
    subject = Subject.objects.get(name=request.session["name"])
    situation_index = get_situation_index(question_index)
    attribute_num = 4+2*situation_index
    if request.method == "POST":
        answered_choice = request.POST["choice"]
        answered_score = request.POST["score"]
        answered_ignore = request.POST["ignore"]
        choice = Choice(
            attribute_num=attribute_num, 
            choice=answered_choice, 
            score=answered_score, 
            ignore=answered_ignore, 
            subject=subject
        )
        choice.save()
        return HttpResponseRedirect(reverse("choice:task", args=[question_index+1]))
    
    if question_index == 60:
        return HttpResponseRedirect(reverse("choice:description2"))
    pair_index = question_index % 15
    player_index_A = 6*situation_index+pairs[pair_index][0]
    player_index_B = 6*situation_index+pairs[pair_index][1]
    players = Player.objects.all()
    return render(request, "choice/task.html", {
        "question_index": question_index, 
        "situation_index": situation_index, 
        "alternative_A": players[player_index_A], 
        "alternative_B": players[player_index_B]
    })


def compare(request):
    subject = Subject.objects.get(name=request.session["name"])
    if request.method == "POST":
        choices_1 = [
            request.POST["choice-1-1"], 
            request.POST["choice-1-2"],
            request.POST["choice-1-3"],
            request.POST["choice-1-4"],
            request.POST["choice-1-5"],
            request.POST["choice-1-6"],
            request.POST["choice-1-7"],
            request.POST["choice-1-8"],
            request.POST["choice-1-9"]
            ]
        choices_2 = [
            request.POST["choice-2-1"], 
            request.POST["choice-2-2"],
            request.POST["choice-2-3"],
            request.POST["choice-2-4"],
            request.POST["choice-2-5"],
            request.POST["choice-2-6"],
            request.POST["choice-2-7"],
            request.POST["choice-2-8"]
            ]
        choices_3 = [
            request.POST["choice-3-1"], 
            request.POST["choice-3-2"],
            request.POST["choice-3-3"],
            request.POST["choice-3-4"],
            request.POST["choice-3-5"],
            request.POST["choice-3-6"],
            request.POST["choice-3-7"]
            ]
        choices_4 = [
            request.POST["choice-4-1"], 
            request.POST["choice-4-2"],
            request.POST["choice-4-3"],
            request.POST["choice-4-4"],
            request.POST["choice-4-5"],
            request.POST["choice-4-6"]
            ]
        choices_5 = [
            request.POST["choice-5-1"], 
            request.POST["choice-5-2"],
            request.POST["choice-5-3"],
            request.POST["choice-5-4"],
            request.POST["choice-5-5"]
            ]
        choices_6 = [
            request.POST["choice-6-1"], 
            request.POST["choice-6-2"],
            request.POST["choice-6-3"],
            request.POST["choice-6-4"]
            ]
        choices_7 = [
            request.POST["choice-7-1"], 
            request.POST["choice-7-2"],
            request.POST["choice-7-3"]
            ]
        choices_8 = [
            request.POST["choice-8-1"], 
            request.POST["choice-8-2"]
            ]
        choices_9 = [
            request.POST["choice-9-1"]
            ]
        
        scores_1 = [
            request.POST["score-1-1"], 
            request.POST["score-1-2"],
            request.POST["score-1-3"],
            request.POST["score-1-4"],
            request.POST["score-1-5"],
            request.POST["score-1-6"],
            request.POST["score-1-7"],
            request.POST["score-1-8"],
            request.POST["score-1-9"]
            ]
        scores_2 = [
            request.POST["score-2-1"], 
            request.POST["score-2-2"],
            request.POST["score-2-3"],
            request.POST["score-2-4"],
            request.POST["score-2-5"],
            request.POST["score-2-6"],
            request.POST["score-2-7"],
            request.POST["score-2-8"]
            ]
        scores_3 = [
            request.POST["score-3-1"], 
            request.POST["score-3-2"],
            request.POST["score-3-3"],
            request.POST["score-3-4"],
            request.POST["score-3-5"],
            request.POST["score-3-6"],
            request.POST["score-3-7"]
            ]
        scores_4 = [
            request.POST["score-4-1"], 
            request.POST["score-4-2"],
            request.POST["score-4-3"],
            request.POST["score-4-4"],
            request.POST["score-4-5"],
            request.POST["score-4-6"]
            ]
        scores_5 = [
            request.POST["score-5-1"], 
            request.POST["score-5-2"],
            request.POST["score-5-3"],
            request.POST["score-5-4"],
            request.POST["score-5-5"]
            ]
        scores_6 = [
            request.POST["score-6-1"], 
            request.POST["score-6-2"],
            request.POST["score-6-3"],
            request.POST["score-6-4"]
            ]
        scores_7 = [
            request.POST["score-7-1"], 
            request.POST["score-7-2"],
            request.POST["score-7-3"]
            ]
        scores_8 = [
            request.POST["score-8-1"], 
            request.POST["score-8-2"]
            ]
        scores_9 = [
            request.POST["score-9-1"]
            ]

        choices = [choices_1, choices_2, choices_3, choices_4, choices_5, choices_6, choices_7, choices_8, choices_9]
        scores = [scores_1, scores_2, scores_3, scores_4, scores_5, scores_6, scores_7, scores_8, scores_9]
        
        evaluate_matrix = get_evaluate_matrix(choices, scores)
        weights = get_weight(evaluate_matrix)
        weight = Weight(
            avg=weights[0], 
            hr=weights[1], 
            sb=weights[2], 
            defense =weights[3], 
            rbi=weights[4], 
            bb=weights[5], 
            risp=weights[6], 
            dp=weights[7], 
            disabled=weights[8], 
            age=weights[9], 
            subject=subject
        )
        weight.save()
        return HttpResponseRedirect(reverse("choice:finish"))

    return render(request, "choice/compare.html", {})

def finish(request):
    return render(request, "choice/finish.html", {})

# make all profiles
def make(request):
    import random
    if request.method == "POST":
        # 6 profiles for each 4 situations
        for i in range(24):
            random_numbers = [random.randint(0, 49) for i in range(12)]
            player = Player(
                avg=values["avg"][random_numbers[0]], 
                hr=values["hr"][random_numbers[1]], 
                sb=values["sb"][random_numbers[2]], 
                defense=values["defense"][random_numbers[3]], 
                rbi=values["rbi"][random_numbers[4]], 
                bb=values["bb"][random_numbers[5]], 
                risp=values["risp"][random_numbers[6]], 
                dp=values["dp"][random_numbers[7]], 
                disabled=values["disabled"][random_numbers[8]], 
                age=values["age"][random_numbers[9]]
            )
            player.save()
        return HttpResponseRedirect(reverse("choice:index"))
    
    return render(request, "choice/make.html", {})