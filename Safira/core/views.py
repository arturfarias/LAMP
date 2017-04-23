from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse 
from .forms import RegisterForm

def index(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(reverse('central'))
        else:
            return render(request, "core/index.html", {"form": form})
    return render(request, "core/index.html",{"form": AuthenticationForm()})

def central(request):
    return render(request,"core/central.html")

def register(request):
#form de cadastro
    context = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('central'))
    else:
        form = RegisterForm()
    return render (request,"core/register.html",{"form": form})
