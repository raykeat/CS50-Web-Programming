from django.urls import path

from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("<int:flight_id>",views.flight,name="flight"),

    #to book a flight for a passenger
    path("<int:flight_id>/book/",views.book,name="book")
    
]