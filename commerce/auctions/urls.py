from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("see_listing/<int:listing_id>", views.see_listing, name="see_listing"),
    path("user_listings", views.user_listings, name="user_listings"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close_auction"),
    path("category/<str:category>", views.check_category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add/<int:listing_id>", views.add2watchlist, name="add2watchlist"),
    path("watchlist/remove/<int:listing_id>", views.removefromwatchlist, name="removefromwatchlist"),
    path("comment/<int:listing_id>", views.comment, name="comment")
]
