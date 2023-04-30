from django.urls import path

from . import views 


#In Django, the app_name variable is used in the urls.py file of an application to specify the 
#namespace for the URLs defined in that application. The namespace helps to differentiate the URLs 
#of different applications in the project.

#When you define the app_name variable in the urls.py file of a Django application, you're essentially 
#creating a unique identifier for the application's URLs.

app_name = "tasks"
urlpatterns = [
    path("",views.index,name="index"),
    path("add",views.add,name="add"),

]