from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import tweet
import traceback
from django.contrib.auth.models import User
from django.contrib import messages

@login_required
def index(request):
    if request.user.is_anonymous:
        return render(request,'form.html')
    
    tweets = tweet.objects.all()
    return render(request, 'index.html', {'tweets': tweets})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirm = request.POST.get('confirm', '').strip()

        user = User.objects.create_user(username=username, password=password)
        auth_login(request, user)
        
        return redirect('index')

    return render(request, 'register.html')


def add_tweet(request):
    if request.method == 'POST':
        try:
            tittle = request.POST.get('tittle', '').strip()
            desc = request.POST.get('desc', '').strip()
            image = request.FILES.get('image')

            
            if not tittle:
                messages.error(request,"title is compulsory")
            if not desc:
                return render(request, 'add.html', {'error': 'Description is required.'})

            tweet.objects.create(tittle=tittle, desc=desc, imag=image)
            return redirect('index')

        except Exception as e:
            print(f"ERROR creating tweet: {e}")
            traceback.print_exc()
            return render(request, 'add.html', {'error': f'Something went wrong: {e}'})
    else:
        return render(request, 'add.html')


def delete_tweet(request, tweet_id):
    t = get_object_or_404(tweet, id=tweet_id)
    if request.method == 'POST':
        t.delete()
    return redirect('index')




def edit_tweet(request, tweet_id):
    t = get_object_or_404(tweet, id=tweet_id)

    if request.method == "POST":
        t.tittle = request.POST.get('tittle', '').strip()
        t.desc = request.POST.get('desc', '').strip()

        if request.FILES.get('image'):
            t.imag = request.FILES.get('image')

        t.save()
        return redirect('index')

    return render(request, 'edit_tweet.html', {'t': t})
def form(request):
    return render(request,'form.html')
def login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username="username",password="password")
        if user is not None:
            login(request,user)
            return redirect('index/')
        else:
            return render(request, "form.html", {
                "error": "Invalid username or password"
            })
    return render(request,'form.html')



            
      

