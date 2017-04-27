from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .decorators import  is_aluno,is_professor
from .models import AlunosMatriculados

def index(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, "core/index.html", {"form": form})
    return render(request, "core/index.html",{"form": AuthenticationForm()})

@login_required
def home(request):
    if request.user.is_staff:
         return HttpResponseRedirect("/admin/")
    elif request.user.has_perm('core.view_professor'):
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
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegisterForm()
    return render (request,"core/register.html",{"form": form})

@is_aluno()
@login_required
def Aluno_disciplina(request):
    disciplinafiltro = AlunosMatriculados.objects.filter(aluno=request.user.id)
    paginator = Paginator(disciplinafiltro, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        disciplinas = paginator.page(page)
    except (EmptyPage, InvalidPage):
        disciplinas = paginator.page(paginator.num_pages)

    return render(request,"core/minhas_disciplinas.html",{'disciplinas':disciplinas})
