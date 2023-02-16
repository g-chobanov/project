from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import RegisterUserForm

# Create your views here.
@login_required(login_url='/login')
def index(request):
    return render(request,'homescreen.html')

def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(index)
    else:
        form = RegisterUserForm()
    context = {
        'form': form
    }
    return render(request, 'registration/registration.html', context)
