from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting",views.createnewlisting, name="newlisting"),
    path("<int:id>/",views.specificlisting,name="specificlisting"),
    path("bid/",views.bid,name="bid"),
    path("closeauction/",views.closeauction,name="closeauction"),
    path("comment/",views.addcomment,name="comment"),
    path("watchlist/",views.watchlist,name="watchlist"),
    path("categorieslist/",views.categorieslist,name="categorieslist"),
    path("category/<str:category>",views.category,name="category"),
]
