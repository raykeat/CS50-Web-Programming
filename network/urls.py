
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("editpost/<int:id>/",views.editpost,name="editpost"),
    path("profile<str:username>/",views.profile,name="profile"),
    path("followuser/<str:currentuser>/<str:userprofile>/",views.followuser,name="followuser"),
    path("unfollowuser/<str:currentuser>/<str:userprofile>/",views.unfollowuser,name="unfollowuser"),
    path("following/<int:id>",views.following,name="following"),
    path("like/<int:postid>/<int:userid>/",views.like,name="like"),
    path("unlike/<int:postid>/<int:userid>/",views.unlike,name="unlike"),
]
