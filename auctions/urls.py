from django.urls import path
from django.contrib import admin


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("add_watchl", views.add_watchl, name="add_watchl"),
    path("remove_watchl", views.remove_watchl, name="remove_watchl"),
    path("make_bid", views.make_bid, name="make_bid"),
    path("end_auction", views.end_auction, name="end_auction"),
]