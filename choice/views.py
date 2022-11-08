from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings

from .models import Subject, Choice, Player, Weight, Preference

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
    "hr": [round(3.4+(0.4*i), 1) for i in range(50)], 
    "sb": [round(0.8+(0.8*i), 1) for i in range(50)], 
    "defense": [round(35.3+(0.6*i), 1) for i in range(50)], 
    "rbi": [round(20.3+(1.3*i), 1) for i in range(50)], 
    "bb": [round(11.2+(1.2*i), 1) for i in range(50)], 
    "risp": [round(0.162+(0.004*i), 3) for i in range(50)], 
    "dp": [round(0.7+(0.7*i), 1) for i in range(50)], 
    "disabled": [round(5.2+(0.4*i), 1) for i in range(50)], 
    "age": [round(20.5+(0.5*i), 1) for i in range(50)]
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

def get_CI(_evaluate_matrix):
  from scipy.linalg import eig
  value, vector = eig(_evaluate_matrix)
  max_lambda = max(value).real
  CI = (max_lambda-len(_evaluate_matrix)) / (len(_evaluate_matrix)-1)
  return CI


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
def description3(request):
    return render(request, "choice/description3.html", {})

# main function
def task(request, question_index):
    subjects = Subject.objects.filter(name=request.session["name"])
    if len(subjects) == 1:
        subject = subjects[0]
    situation_index = get_situation_index(question_index)
    attribute_num = 4+2*situation_index
    if request.method == "POST":
        answered_choice = request.POST["choice"]
        answered_score = int(request.POST["score"])
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
        "question_index_p1": question_index+1, 
        "situation_index": situation_index, 
        "alternative_A": players[player_index_A], 
        "alternative_B": players[player_index_B]
    })


def compare(request):
    subjects = Subject.objects.filter(name=request.session["name"])
    subject = subjects[0]
    if request.method == "POST":
        choices_1 = [
            int(request.POST["choice-1-1"]), 
            int(request.POST["choice-1-2"]),
            int(request.POST["choice-1-3"]),
            int(request.POST["choice-1-4"]),
            int(request.POST["choice-1-5"]),
            int(request.POST["choice-1-6"]),
            int(request.POST["choice-1-7"]),
            int(request.POST["choice-1-8"]),
            int(request.POST["choice-1-9"])
            ]
        choices_2 = [
            int(request.POST["choice-2-1"]), 
            int(request.POST["choice-2-2"]),
            int(request.POST["choice-2-3"]),
            int(request.POST["choice-2-4"]),
            int(request.POST["choice-2-5"]),
            int(request.POST["choice-2-6"]),
            int(request.POST["choice-2-7"]),
            int(request.POST["choice-2-8"])
            ]
        choices_3 = [
            int(request.POST["choice-3-1"]), 
            int(request.POST["choice-3-2"]),
            int(request.POST["choice-3-3"]),
            int(request.POST["choice-3-4"]),
            int(request.POST["choice-3-5"]),
            int(request.POST["choice-3-6"]),
            int(request.POST["choice-3-7"])
            ]
        choices_4 = [
            int(request.POST["choice-4-1"]), 
            int(request.POST["choice-4-2"]),
            int(request.POST["choice-4-3"]),
            int(request.POST["choice-4-4"]),
            int(request.POST["choice-4-5"]),
            int(request.POST["choice-4-6"])
            ]
        choices_5 = [
            int(request.POST["choice-5-1"]), 
            int(request.POST["choice-5-2"]),
            int(request.POST["choice-5-3"]),
            int(request.POST["choice-5-4"]),
            int(request.POST["choice-5-5"])
            ]
        choices_6 = [
            int(request.POST["choice-6-1"]), 
            int(request.POST["choice-6-2"]),
            int(request.POST["choice-6-3"]),
            int(request.POST["choice-6-4"])
            ]
        choices_7 = [
            int(request.POST["choice-7-1"]), 
            int(request.POST["choice-7-2"]),
            int(request.POST["choice-7-3"])
            ]
        choices_8 = [
            int(request.POST["choice-8-1"]), 
            int(request.POST["choice-8-2"])
            ]
        choices_9 = [
            int(request.POST["choice-9-1"])
            ]
        
        scores_1 = [
            int(request.POST["score-1-1"]), 
            int(request.POST["score-1-2"]),
            int(request.POST["score-1-3"]),
            int(request.POST["score-1-4"]),
            int(request.POST["score-1-5"]),
            int(request.POST["score-1-6"]),
            int(request.POST["score-1-7"]),
            int(request.POST["score-1-8"]),
            int(request.POST["score-1-9"])
            ]
        scores_2 = [
            int(request.POST["score-2-1"]), 
            int(request.POST["score-2-2"]),
            int(request.POST["score-2-3"]),
            int(request.POST["score-2-4"]),
            int(request.POST["score-2-5"]),
            int(request.POST["score-2-6"]),
            int(request.POST["score-2-7"]),
            int(request.POST["score-2-8"])
            ]
        scores_3 = [
            int(request.POST["score-3-1"]), 
            int(request.POST["score-3-2"]),
            int(request.POST["score-3-3"]),
            int(request.POST["score-3-4"]),
            int(request.POST["score-3-5"]),
            int(request.POST["score-3-6"]),
            int(request.POST["score-3-7"])
            ]
        scores_4 = [
            int(request.POST["score-4-1"]), 
            int(request.POST["score-4-2"]),
            int(request.POST["score-4-3"]),
            int(request.POST["score-4-4"]),
            int(request.POST["score-4-5"]),
            int(request.POST["score-4-6"])
            ]
        scores_5 = [
            int(request.POST["score-5-1"]), 
            int(request.POST["score-5-2"]),
            int(request.POST["score-5-3"]),
            int(request.POST["score-5-4"]),
            int(request.POST["score-5-5"])
            ]
        scores_6 = [
            int(request.POST["score-6-1"]), 
            int(request.POST["score-6-2"]),
            int(request.POST["score-6-3"]),
            int(request.POST["score-6-4"])
            ]
        scores_7 = [
            int(request.POST["score-7-1"]), 
            int(request.POST["score-7-2"]),
            int(request.POST["score-7-3"])
            ]
        scores_8 = [
            int(request.POST["score-8-1"]), 
            int(request.POST["score-8-2"])
            ]
        scores_9 = [
            int(request.POST["score-9-1"])
            ]

        choices = [choices_1, choices_2, choices_3, choices_4, choices_5, choices_6, choices_7, choices_8, choices_9]
        scores = [scores_1, scores_2, scores_3, scores_4, scores_5, scores_6, scores_7, scores_8, scores_9]
        
        evaluate_matrix = get_evaluate_matrix(choices, scores)
        weights = get_weight(evaluate_matrix)
        CI = get_CI(evaluate_matrix)
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
            CI=CI, 
            subject=subject
        )
        weight.save()
        return HttpResponseRedirect(reverse("choice:description3"))

    return render(request, "choice/compare.html", {})

def preference(request):
    subjects = Subject.objects.filter(name=request.session["name"])
    subject = subjects[0]
    if request.method == "POST":
        choices_1 = [
            int(request.POST["choice-1-1"]), 
            int(request.POST["choice-1-2"]),
            int(request.POST["choice-1-3"])
            ]
        choices_2 = [
            int(request.POST["choice-2-1"]), 
            int(request.POST["choice-2-2"])
            ]
        choices_3 = [
            int(request.POST["choice-3-1"])
            ]
        
        scores_1 = [
            int(request.POST["score-1-1"]), 
            int(request.POST["score-1-2"]),
            int(request.POST["score-1-3"])
            ]
        scores_2 = [
            int(request.POST["score-2-1"]), 
            int(request.POST["score-2-2"])
            ]
        scores_3 = [
            int(request.POST["score-3-1"])
            ]

        choices = [choices_1, choices_2, choices_3]
        scores = [scores_1, scores_2, scores_3]
        
        evaluate_matrix = get_evaluate_matrix(choices, scores)
        preferences = get_weight(evaluate_matrix)
        CI = get_CI(evaluate_matrix)
        preference = Preference(
            four=preferences[0], 
            six=preferences[1], 
            eight=preferences[2], 
            ten=preferences[3], 
            CI=CI, 
            subject=subject
        )
        preference.save()
        return HttpResponseRedirect(reverse("choice:finish"))

    return render(request, "choice/preference.html", {})

def finish(request):
    return render(request, "choice/finish.html", {})

# make all profiles
def make(request):
    four = {
        'avg': [0.26, 0.226, 0.276, 0.3, 0.22, 0.222], 
        'hr': [12.6, 14.2, 15, 23, 8.2, 14.6], 
        'sb': [7.2, 24, 36, 36.8, 37.6, 3.2], 
        'defense': [58.1, 46.1, 36.5, 36.5, 64.7, 62.9], 
        'rbi': [59.3, 54.1, 68.4, 51.5, 73.6, 42.4], 
        'bb': [14.8, 23.2, 22, 62.8, 29.2, 58], 
        'risp': [0.214, 0.33, 0.21, 0.206, 0.166, 0.314], 
        'dp': [35, 32.9, 3.5, 18.9, 16.1, 19.6], 
        'disabled': [14, 23.2, 8, 20, 24.4, 6.8], 
        'age': [31, 40.5, 38, 39.5, 29.5, 41]
    }
    six = {
        'avg': [0.312, 0.302, 0.294, 0.306, 0.224, 0.286], 
        'hr': [13.4, 9.4, 21, 22.2, 9.8, 10.6], 
        'sb': [21.6, 34.4, 16, 36, 11.2, 40], 
        'defense': [52.7, 41.3, 54.5, 53.9, 56.9, 38.9], 
        'rbi': [41.1, 47.6, 35.9, 77.5, 59.3, 20.3], 
        'bb': [22, 24.4, 70, 28, 58, 14.8], 
        'risp': [0.214, 0.33, 0.21, 0.206, 0.166, 0.314], 
        'dp': [35, 32.9, 3.5, 18.9, 16.1, 19.6], 
        'disabled': [14, 23.2, 8, 20, 24.4, 6.8], 
        'age': [31, 40.5, 38, 39.5, 29.5, 41]
    }
    eight = {
        'avg': [0.296, 0.224, 0.31, 0.254, 0.23, 0.254], 
        'hr': [5.4, 20.2, 8.6, 15.8, 22.2, 13], 
        'sb': [25.6, 14.4, 12.8, 18.4, 7.2, 31.2], 
        'defense': [43.7, 41.3, 64.7, 44.3, 61.7, 55.1], 
        'rbi': [61.9, 77.5, 52.8, 82.7, 80.1, 22.9], 
        'bb': [23.2, 26.8, 37.6, 22, 43.6, 43.6], 
        'risp': [0.21, 0.234, 0.238, 0.302, 0.202, 0.25], 
        'dp': [25.9, 6.3, 7, 16.1, 11.2, 8.4], 
        'disabled': [14, 23.2, 8, 20, 24.4, 6.8], 
        'age': [31, 40.5, 38, 39.5, 29.5, 41]
    }
    ten = {
        'avg': [0.286, 0.288, 0.296, 0.232, 0.264, 0.23], 
        'hr': [6.6, 15.4, 14.6, 19, 13, 19.8], 
        'sb': [18.4, 26.4, 36, 5.6, 16.8, 35.2], 
        'defense': [49.7, 54.5, 40.1, 43.1, 53.9, 39.5], 
        'rbi': [59.3, 54.1, 68.4, 51.5, 73.6, 42.4], 
        'bb': [14.8, 23.2, 22, 62.8, 29.2, 58], 
        'risp': [0.214, 0.33, 0.21, 0.206, 0.166, 0.314], 
        'dp': [35, 32.9, 3.5, 18.9, 16.1, 19.6], 
        'disabled': [14, 23.2, 8, 20, 24.4, 6.8], 
        'age': [31, 40.5, 38, 39.5, 29.5, 41]
    }

    import random
    if request.method == "POST":
        # 6 profiles for each 4 situations
        for i in range(6):
            player = Player(
                avg=four["avg"][i], 
                hr=four["hr"][i], 
                sb=four["sb"][i], 
                defense=four["defense"][i], 
                rbi=four["rbi"][i], 
                bb=four["bb"][i], 
                risp=four["risp"][i], 
                dp=four["dp"][i], 
                disabled=four["disabled"][i], 
                age=four["age"][i]
            )
            player.save()
        for i in range(6):
            player = Player(
                avg=six["avg"][i], 
                hr=six["hr"][i], 
                sb=six["sb"][i], 
                defense=six["defense"][i], 
                rbi=six["rbi"][i], 
                bb=six["bb"][i], 
                risp=six["risp"][i], 
                dp=six["dp"][i], 
                disabled=six["disabled"][i], 
                age=six["age"][i]
            )
            player.save()
        for i in range(6):
            player = Player(
                avg=eight["avg"][i], 
                hr=eight["hr"][i], 
                sb=eight["sb"][i], 
                defense=eight["defense"][i], 
                rbi=eight["rbi"][i], 
                bb=eight["bb"][i], 
                risp=eight["risp"][i], 
                dp=eight["dp"][i], 
                disabled=eight["disabled"][i], 
                age=eight["age"][i]
            )
            player.save()
        for i in range(6):
            player = Player(
                avg=ten["avg"][i], 
                hr=ten["hr"][i], 
                sb=ten["sb"][i], 
                defense=ten["defense"][i], 
                rbi=ten["rbi"][i], 
                bb=ten["bb"][i], 
                risp=ten["risp"][i], 
                dp=ten["dp"][i], 
                disabled=ten["disabled"][i], 
                age=ten["age"][i]
            )
            player.save()

        return HttpResponseRedirect(reverse("choice:index"))
    
    return render(request, "choice/make.html", {})