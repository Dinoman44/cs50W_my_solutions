from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("disease-list", views.disease_list, name="disease list(old)"),
    path("disorder-list", views.disease_list, name="disease list"),
    path("nutrient-list", views.nutrient_list, name="nutrient list"),
    path("food-list", views.food_list, name="food list"),
    path("disease/<str:disease_ID>", views.disease_info, name="disease_info(old)"),
    path("disorder/<str:disease_ID>", views.disease_info, name="disease_info"),
    path("nutrient/<str:nutrient_ID>", views.nutrient_info, name="nutrient_info"),
    path("pizza-prefs", views.pizza_prefs, name="pizza prefs"),
    path("pizza-gen", views.generate_pizza, name="pizza gen"),
    path("request_info", views.request_info, name="request info")
]