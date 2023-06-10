from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Posts
from datetime import datetime
from django.core.paginator import Paginator


def index(request):
    if request.method=="POST":
        postcontent = request.POST.get('newpostcontent')
        submissiontime = datetime.now()
        Posts.objects.create(username = request.user, content=postcontent, submissiontime=submissiontime)

        #pagination showing 10 posts per page
        paginator = Paginator(Posts.objects.order_by('-submissiontime'), 10) 
        page_number = request.GET.get('page')
        pageposts = paginator.get_page(page_number)

        return render(request, "network/index.html",{
            "posts":pageposts
        })

        
    #if request.method=="GET"
    else:
        #pagination showing 10 posts per page
        paginator = Paginator(Posts.objects.order_by('-submissiontime'), 10) 
        page_number = request.GET.get('page')
        pageposts = paginator.get_page(page_number)
        return render(request, "network/index.html",{
            "posts":pageposts
        })

def profile(request,username):
        user = User.objects.get(username=username)
        #pagination show 10 posts per page.
        paginator = Paginator(Posts.objects.filter(username = user).order_by('-submissiontime'), 10) 
        page_number = request.GET.get('page')
        pageposts = paginator.get_page(page_number)

        #getting followers and following count
        followers = user.followers.count()
        following = user.following.count()

        #checking if current user is following user whose profile is being checked out
        currentuser = User.objects.get(username=request.user.username)
        if currentuser in user.followers.all():
            is_follower = True
        else:
            is_follower = False


        return render(request, "network/profile.html",{
            "posts":pageposts,
            "followers":followers,
            "following":following,
            "userprofile":username,
            "is_follower":is_follower
        })

def followuser(request,currentuser,userprofile):
    CurrentUser = User.objects.get(username=currentuser)
    UserProfile = User.objects.get(username=userprofile)

    #adding CurrentUser to UserProfile's followers, and updating follower count
    UserProfile.followers.add(CurrentUser)
    UserProfile.save()
    followers = UserProfile.followers.count()

    #Adding Userprofile to current user's following list
    CurrentUser.following.add(UserProfile)
    CurrentUser.save()
    #return JSON response to AJAX request
    return JsonResponse({"followers":followers})
    

def unfollowuser(request,currentuser,userprofile):
    CurrentUser = User.objects.get(username=currentuser)
    UserProfile = User.objects.get(username=userprofile)

    #removing CurrentUser from UserProfile's followers, and updating follower count
    UserProfile.followers.remove(CurrentUser)
    UserProfile.save()
    followers = UserProfile.followers.count()

    #Removing Userprofile from current user's following list
    CurrentUser.following.remove(UserProfile)
    CurrentUser.save()
    #return JSON response to AJAX request
    return JsonResponse({"followers":followers})
    
def following(request,id):
    currentuser = User.objects.get(id=id)
    following = currentuser.following.all()
    posts = Posts.objects.filter(username__in=following)

    #pagination showing 10 posts per page
    paginator = Paginator(posts.order_by('-submissiontime'), 10) 
    page_number = request.GET.get('page')
    pageposts = paginator.get_page(page_number)

    return render(request,"network/following.html",{
        "posts":pageposts
    })

from django.views.decorators.http import require_http_methods

@require_http_methods(["PUT","POST"])
def editpost(request,id):
    if request.method == "PUT":
    
        data = json.loads(request.body)
        post=Posts.objects.get(pk=id)
        post.content = data["content"]
        post.save()

        #Return JSON response indicating success
        response_data = {
            'status': 'success',
            'message': 'Post content updated successfully.',
        }
        return JsonResponse(response_data)
    
def like(request, postid, userid):
    if request.method == "PUT":
        post=Posts.objects.get(id=postid)
        user=User.objects.get(id=userid)
        post.users_who_liked.add(user)
        post.likecount+=1
        post.save()

        

        # Return JSON response indicating success
        response_data = {
            'status': 'success',
            'likecount':post.likecount,
        }
        return JsonResponse(response_data)
    
def unlike(request, postid, userid):
    if request.method == "PUT":
        post=Posts.objects.get(id=postid)
        user=User.objects.get(id=userid)
        post.users_who_liked.remove(user)
        post.likecount-=1
        post.save()

        

        # Return JSON response indicating success
        response_data = {
            'status': 'success',
            'likecount':post.likecount,
        }
        return JsonResponse(response_data)

    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
