from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("search", views.search, name="search"),
    path("random", views.random, name="random"),
    path("new_page", views.new_page, name="new_page"),
    path("edit", views.edit_page, name="edit")
]
