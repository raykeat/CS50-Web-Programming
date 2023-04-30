from django.urls import path

from . import views 

urlpatterns = [
    path("",views.index,name="index"),
    path("ray", views.ray,name="ray"),
    path("<str:name>",views.greet,name="greet")

]