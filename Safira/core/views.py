from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import RegisterForm
from .models import Professor, Aluno

def index(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, "core/index.html", {"form": form})
    return render(request, "core/index.html",{"form": AuthenticationForm()})

def home(request):
    if request.user.has_perm('core.view_professor'):
        return redirect(reverse('professor'))
    elif request.user.has_perm('core.view_aluno'):
        return redirect(reverse('aluno'))

def register(request):
#form de cadastro
    context = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = RegisterForm()
    return render (request,"core/register.html",{"form": form})

def aluno(request):
    return render(request,"core/aluno.html")

def professor(request):
    return render(request,"core/professor.html")
