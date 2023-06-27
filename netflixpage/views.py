from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import User, Movies, Genres
import requests, os
from django.http import JsonResponse
import requests


class NewTaskForm(forms.Form):
    username = forms.CharField(label="username", widget=forms.TextInput(attrs={'class': 'rounded-lg opacity-75 bg-white text-black text-bold'}))
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={'class': 'rounded-lg opacity-75 bg-white text-black text-bold'}))
    confirmpassword = forms.CharField(label="confirm password", widget=forms.PasswordInput(attrs={'class': 'rounded-lg opacity-75 bg-white text-black text-bold'}))
    email = forms.CharField(label="email", widget=forms.EmailInput(attrs={'class': 'rounded-lg opacity-75 bg-white text-black text-bold'}))

class SignInForm(forms.Form):
    username = forms.CharField(label="username", widget=forms.TextInput(attrs={'class': 'rounded-lg opacity-75 bg-white text-black text-bold'}))
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={'class': 'rounded-lg opacity-75 bg-white text-black text-bold'}))
    email = forms.CharField(label="email", widget=forms.EmailInput(attrs={'class': 'rounded-lg opacity-75 bg-white text-black text-bold'}))

# Create your views here.
def index(request):
    return render(request,"netflixpage/index.html",{
})

#to retrieve movie data using TMDB API
def retrieve(request):
    
    #saving genres and their respective ids into backend Genres database
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
    headers = {
        "accept": "application/json",
        #FOR CS50 GRADING STAFF, YOU MUST OBTAIN YOUR OWN HEADERS AUTHORIZATION BY
        #SIGNING UP FOR AN ACCOUNT AT https://developer.themoviedb.org/reference/genre-movie-list
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkMWQzMTg2M2RjNjg2ZDJkZTZiMDFiYzFkMjU4NGIyMyIsInN1YiI6IjY0OGRlNzUzMjYzNDYyMDE0ZTU3YzVhNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Dwpm5j_yAILTOKx93IPc5dj8rabkxx-ea7lgpD0ajdE"
    }
    response = requests.get(url, headers=headers)
    jsonresponse = response.json()
    #accessing value of "genres" key
    genres_data = jsonresponse['genres']
    for genre in genres_data:
        existinggenre = Genres.objects.filter(genreid= genre['id'],genre= genre['name']).first()
        if existinggenre:
            continue
        Genres(genreid= genre['id'],genre= genre['name']).save()



    #fetch real time movie data from TMDB Database before saving it into Movies Model
    movies = []
    n=0
    while n<1:
        n+=1
        url = "https://api.themoviedb.org/3/discover/movie?api_key=d1d31863dc686d2de6b01bc1d2584b23&include_adult=false&include_video=true&language=en-US&page={}&offset=20&sort_by=popularity.desc&with_genres=27".format(n)
        response = requests.get(url)
        jsonresponse = response.json()
        movies.extend(jsonresponse['results'])
    
    for movie in movies:
        movieid = movie['id']
        title = movie['title']
        overview = movie['overview']
        genre_ids = movie['genre_ids']
        rating = movie['vote_average']
        poster_path = movie['poster_path']
        release_date = movie['release_date']

        #additional API request to retrieve short videos/trailers for each movie
        video_url = f"https://api.themoviedb.org/3/movie/{movieid}/videos?api_key=d1d31863dc686d2de6b01bc1d2584b23"
        response = requests.get(video_url)
        jsonresponse = response.json()
        if len(jsonresponse['results'])>0:
            #Retrieve key of first video
            video_key = jsonresponse['results'][0]['key']
            # Construct YouTube embed url
            embed_url = f"https://www.youtube.com/embed/{video_key}"


        #create a new movie object if movie doesn't yet exist in backend django model/database
        if not Movies.objects.filter(movieid=movieid).exists():
            newmovie = Movies(title=title,overview=overview,rating=rating,releasedate=release_date,movieid=movieid,embedurl=embed_url)
            newmovie.save()

            #getting genres corresponding to genre_ids
            #getting genreobjects whose genreid is in genre_ids retrieved from TMDB API
            genre_ids = movie['genre_ids']
            genreobjects = Genres.objects.filter(genreid__in=genre_ids)
            genre_names = [genreobject.genre for genreobject in genreobjects]
            newmovie.genres = ", ".join(genre_names)
            newmovie.save()

            """saving the image found at poster path to project directory"""
            image_url = 'https://image.tmdb.org/t/p/w500' + poster_path
            response = requests.get(image_url)

            #if request is successful
            if response.status_code == 200:
                # Create a directory to store the images if it doesn't exist
                os.makedirs(r'C:\Users\teohr\Downloads\netflixclone\netflixpage\static\netflixpage', exist_ok=True)

                # Get the file name from the image URL
                file_name = os.path.basename(image_url)

                # Save the image to the specified directory
                image_path = os.path.join(r'C:\Users\teohr\Downloads\netflixclone\netflixpage\static\netflixpage', file_name)
                #with open(image_path, 'wb') as f:
                    #f.write(response.content)

                #save the image path to the new_movie object 
                newmovie.posterpath = image_url
                newmovie.save()
    
    #response data when react components make fetch request to backend here
    movies_data=[]
    for movie in Movies.objects.all():

        #checking if movie has been liked by user
        if not movie in request.user.liked_movies.all():
            liked_button_message = "Like"
        else:
            liked_button_message = "Unlike"
        #checking if movie has been added to watchlist
        if not movie in request.user.watchlist_movies.all():
            watchlist_message = "Add to watchlist"
            watchlist_class = "fa fa-plus"
        else:
            watchlist_message = "Remove from watchlist"
            watchlist_class = "fa fa-minus"
        dictionary = {
            'title':movie.title,
            'overview':movie.overview,
            'rating':movie.rating,
            'releasedate':movie.releasedate,
            'genres':movie.genres,
            'posterpath':movie.posterpath,
            'movieid':movie.movieid,
            "liked_button_message": liked_button_message,
            "watchlist_message":watchlist_message,
            "watchlist_class":watchlist_class,
            "embed_url":movie.embedurl,
        }
        movies_data.append(dictionary)
    #JSON response to AJAX requests
    return JsonResponse(movies_data,safe=False)

#rendering watchlist.html
def watchlistmovies(request):
    return render(request,"netflixpage/watchlist.html")

#retrieving movies in user's watchlist
def retrieve_watchlist(request):
    
    #response data when react components make fetch request to backend here
    movies_data=[]
    for movie in request.user.watchlist_movies.all():

        #checking if movie has been liked by user
        if not movie in request.user.liked_movies.all():
            liked_button_message = "Like"
        else:
            liked_button_message = "Unlike"
        #checking if movie has been added to watchlist
        if not movie in request.user.watchlist_movies.all():
            watchlist_message = "Add to watchlist"
            watchlist_class = "fa fa-plus"
        else:
            watchlist_message = "Remove from watchlist"
            watchlist_class = "fa fa-minus"
        dictionary = {
            'title':movie.title,
            'overview':movie.overview,
            'rating':movie.rating,
            'releasedate':movie.releasedate,
            'genres':movie.genres,
            'posterpath':movie.posterpath,
            'movieid':movie.movieid,
            "liked_button_message": liked_button_message,
            "watchlist_message":watchlist_message,
            "watchlist_class":watchlist_class
        }
        movies_data.append(dictionary)
    #JSON response to AJAX requests
    return JsonResponse(movies_data,safe=False)
    

#function to like/unlike movie for user, and to update text in like/unlike button
def like(request, id, message):
    if message == "Like":
        user = request.user
        movie = Movies.objects.get(movieid=id)
        user.liked_movies.add(movie)
        user.save()

        # Return JSON response to update text
        response_data = {
            "liked_message": "Unlike"
        }
        return JsonResponse(response_data)

    else:
        user = request.user
        movie = Movies.objects.get(movieid=id)
        user.liked_movies.remove(movie)
        user.save()

        # Return JSON response to update text
        response_data = {
            "liked_message": "Like"
        }
        return JsonResponse(response_data)

##testpage
def testpage(request):
    return render(request,"netflixpage/testpage.html")


#function to add/remove movie from user's watchlist, and update text in watchlist button  
def watchlist(request, id, message):
    if message == "Add to watchlist":
        movie = Movies.objects.get(movieid=id)
        request.user.watchlist_movies.add(movie)
        request.user.save()

        # Return JSON response to update text
        response_data = {
            "watchlist_message": "Remove from watchlist",
            "watchlist_class":"fa fa-minus"
        }
        return JsonResponse(response_data)
    
    else:
        movie = Movies.objects.get(movieid=id)
        request.user.watchlist_movies.remove(movie)
        request.user.save()

        # Return JSON response to update text
        response_data = {
            "watchlist_message": "Add to watchlist",
            "watchlist_class":"fa fa-plus"
        }
        return JsonResponse(response_data)


def register(request):
    if request.method == "GET":
        email = request.GET.get("email")
        form = NewTaskForm(initial={"email": email})
        return render(request,"netflixpage/register.html",{
            "form":form,
        })
    
    if request.method == "POST":
        # Take in the data the user submitted in registeremail form and save it as form
        form = NewTaskForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            confirmpassword = form.cleaned_data["confirmpassword"]
            email = form.cleaned_data["email"]

            #if passwords do not match, return error message
            if password!=confirmpassword:
                error = "Passwords do not match"
                return render(request,"netflixpage/register.html",{
                "form":form,
                "message":error
                })
            
            #if passwords match, then register user
            else:
                try:
                    user = User.objects.create_user(username, email, password)
                    user.save()
                    login(request, user)
                    return redirect('/')
                except IntegrityError:
                    return render(request, "netflixpage/register.html", {
                        "message": "Username already taken.",
                        "form":form
                    })
                

        
        else:
            return render(request,"netflixpage/register.html",{
            "form":form
        })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def login_view(request):
    if request.method=="GET":
        return render(request,"netflixpage/login.html",{
            "form":SignInForm()
        })

    #if request method is POST
    else:

        # Take in the data the user submitted in signin form and save it as form
        form = SignInForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            #attempt to sign user in
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "netflixpage/login.html", {
                    "message": "Invalid username and/or password."
                })
        
        else:
            return render(request, "netflixpage/login.html", {
                    "form": form
                })
        
        
