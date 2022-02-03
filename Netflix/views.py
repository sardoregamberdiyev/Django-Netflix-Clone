from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from Core.settings import TMDB_API_KEY
import requests
import tmdbsimple as tmdb

# Create your views here.
def Home(request):
    return render(request, 'Index.html')
    
def Register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, '⚠️ Passwords Do Not Match! Try Again')
            return redirect('Register')

        if User.objects.filter(username=username).exists():
            messages.error(request, '⚠️ Username Already Exists! Choose Another One')
            return redirect('Register')

        if User.objects.filter(email=email).exists():
            messages.error(request, '⚠️ Email Address Already Exists! Choose Another One')
            return redirect('Register')

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password1)
        user.save()

        messages.success(request, '✅ Regristration Successful! You can now log in.')
        return redirect('Register')

    return render(request, 'Register.html')

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if not User.objects.filter(username=username).exists():
            messages.error(request, '⚠️ Username Does Not Exist! Choose Another One')
            return redirect('Login')

        if user is None:
            messages.error(request, '⚠️ Username or Password Is Incorrect!! Please Try Again')
            return redirect('Login')

        if user is not None:
            login(request, user)
            return redirect(reverse('Recommendations'))
        
    return render(request, 'Login.html')

@login_required(login_url='Login')
def Logout(request):
    logout(request)
    messages.success(request, '✅ Successfully Logged Out!')
    return redirect(reverse('Login'))

@login_required(login_url='Login')
def Recommendations(request):
    now_playing_movies_request = requests.get("https://api.themoviedb.org/3/movie/now_playing?api_key=" + TMDB_API_KEY)
    now_playing_movies_results = now_playing_movies_request.json()
    now_playing_movies = now_playing_movies_results['results']

    top_rated_shows_request = requests.get("https://api.themoviedb.org/3/tv/top_rated?api_key=" + TMDB_API_KEY)
    top_rated_shows_results = top_rated_shows_request.json()
    top_rated_shows = top_rated_shows_results['results']

    top_rated_request = requests.get("https://api.themoviedb.org/3/movie/top_rated?api_key=" + TMDB_API_KEY)
    top_rated_results = top_rated_request.json()
    top_rated = top_rated_results['results']

    popular_tv_request = requests.get("https://api.themoviedb.org/3/tv/popular?api_key=" + TMDB_API_KEY)
    popular_tv_results = popular_tv_request.json()
    popular_tv = popular_tv_results['results']

    upcoming_request = requests.get("https://api.themoviedb.org/3/movie/upcoming?api_key=" + TMDB_API_KEY)
    upcoming_results = upcoming_request.json()
    upcoming = upcoming_results['results']

    return render(request, 'Recommendations.html', {'now_playing_movies':now_playing_movies, 'top_rated_shows':top_rated_shows, 'top_rated':top_rated, 'upcoming':upcoming, 'popular_tv':popular_tv})