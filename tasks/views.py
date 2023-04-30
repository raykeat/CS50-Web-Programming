from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

tasks=[]

#creating a form class
#forms.Form is a base class in django's web framework, defining a class NewTaskForm that inherits from forms.Form
class NewTaskForm(forms.Form):
    task = forms.CharField(label="Newtask")
    priority = forms.IntegerField(label="Priority",min_value=1,max_value=10)

# Create your views here.

def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "tasks/index.html",{
        "tasks":request.session["tasks"]})

def add(request):
    if request.method =="POST":

        #request.POST contains all of the data the user keyed inside the form when it was submitted
        #essentially creating a form and filling it with all the data the user entered
        form = NewTaskForm(request.POST)
        if form.is_valid():

            #getting data from the task field in the form
            task = form.cleaned_data["task"]
            request.session["tasks"]+=[task]
            return HttpResponseRedirect(reverse("tasks:index"))

            #another way to redirect/return to index.html page
            #return render(request, "tasks/index.html",{
                #"tasks":tasks
            #})
        else:
            return render(request, "tasks/add.html",{
                "form":form
            })
    
    #if request method is get
    else:
        return render(request, "tasks/add.html",{
            "form":NewTaskForm()
        })

