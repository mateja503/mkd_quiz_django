# views.py (in the project folder)
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user automatically
            return redirect('/')  # Redirect to the homepage or desired page
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

from django.shortcuts import render

from django.contrib.auth.decorators import login_required
@login_required
def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')