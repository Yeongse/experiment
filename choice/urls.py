from django.urls import path

from . import views

app_name = "choice"

urlpatterns = [
    path("", views.index, name="index"), 
    path("task/", views.task, name="task"), 
    path("interval", views.interval, name="interval")
]