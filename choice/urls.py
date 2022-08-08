from django.urls import path

from . import views

app_name = "choice"

urlpatterns = [
    path("", views.index, name="index"), 
    path("description1/", views.description1, name="description1"), 
    path("description2/", views.description1, name="description2"), 
    path("task/<int:question_index>", views.task, name="task"), 
    path("compare/", views.compare, name="compare"),
    path("finish/", views.finish, name="finish"), 
    path("make/", views.make, name="make")
]