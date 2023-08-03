from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("user/<int:user_id>", views.see_user, name="see_user"),
    path("following", views.following_page, name="following"),
    path("react", views.like_unlike, name="react"),
    path("edit", views.edit_post, name="edit"),
    path("followstuff", views.followstuff, name="followstuff")
]