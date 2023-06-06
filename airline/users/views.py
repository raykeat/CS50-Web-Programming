from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def index(request):
    #if user is not authenticated ie. if user is not logged in
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request,"users/user.html")

def login_view(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        #if user was successfully authenticated
        if user:
            login(request,user)
            return redirect('index')
        
        # if user was not authenticated
        return render(request,"users/login.html",{
            "message":"Invalid credentials"
        })
    return render(request,"users/login.html")

def logout_view(request):
    logout(request)
    return render (request, "users/login.html",{
        "message":"Logged out Nigga fuck you theodore wang"
    })

        
