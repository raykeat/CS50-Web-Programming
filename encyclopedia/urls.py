from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>",views.general,name="general"),
    path("CSS/",views.CSS,name="CSS"),
    path("Django/",views.Django,name="Django"),
    path("Git/",views.Git,name="Git"),
    path("HTML/",views.HTML,name="HTML"),
    path("Python/",views.HTML,name="Python"),
    path("search/",views.search,name="search"),
    path("newpage/",views.newpage,name="newpage"),

    #<str:title> included here as title was passed in as parameter to url in redirect('newentry', title=title)
    path("newentry/<str:title>",views.newentry,name="newentry"),

    #<str:title> was included here as the title was passed in as parameter to the url when form in editmdcontent.html was submitted
    path("editmdcontent/<str:title>",views.editmdcontent,name="editmdcontent"),
    path("randompage/",views.randompage,name="randompage")

]
