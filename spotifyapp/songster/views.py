from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in

from .forms import RegisterUserForm

@login_required(login_url='/login')
def index(request):
    return render(request,'homescreen.html')

def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('songster:')
    else:
        form = RegisterUserForm()
    context = {
        'form': form
    }
    return render(request, 'registration/registration.html', context)

@receiver(user_logged_in)
def save_session_key(sender, request, user, **kwargs):
    request.session['user_session_key'] = request.session.session_key
