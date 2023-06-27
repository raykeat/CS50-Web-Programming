from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/",views.register,name="register"),
    path("logout/",views.logout_view,name="logout"),
    path("login/",views.login_view,name="login"),

    #Django API Endpoint to retrieve movie data
    path("retrievemovie/homepage/",views.retrieve,name="retrieve"),
    path("retrievemovie/watchlist/",views.retrieve_watchlist,name="retrieve_watchlist"),

    #to like and add to watchlist
    path("like/<int:id>/<str:message>/",views.like,name="like"),
    path("watchlist/<int:id>/<str:message>/",views.watchlist,name="watchlist"),

    #to render watchlist page
    path("watchlistmovies/",views.watchlistmovies,name="watchlistmovies"),


    ##test page
    path("testpage/",views.testpage,name="testpage")

]
