from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, MatriculaForm,DisciplinaForms
from .decorators import  is_aluno,is_professor
from .models import AlunosMatriculados,Aluno,Disciplina,Turma

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
    aluno = Aluno.objects.get(usuario=request.user)
    disciplinafiltro = AlunosMatriculados.objects.filter(aluno_id=aluno,pendencia = False).order_by('turma')
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

@is_aluno()
@login_required
def All_disciplinas(request):
    aluno = Aluno.objects.get(usuario=request.user)
    lista_disciplinas = Disciplina.objects.all().order_by('nome')
    turmas = Turma.objects.all().order_by('semestre')
    paginator = Paginator(lista_disciplinas, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        dis = paginator.page(page)
    except (EmptyPage, InvalidPage):
        dis = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = MatriculaForm(request.POST)
        form = form.save(commit=False)
        form.aluno = aluno
        form.turma = Turma.objects.get(id=request.POST.get("id_turma"))
        form.save()

    return render(request, "core/disciplinas.html",{'dis':dis,'turmas':turmas})

@is_professor()
@login_required
def Professor_disciplina(request):
    disciplinafiltro = Disciplina.objects.filter(creator=request.user).order_by('nome')
    paginator = Paginator(disciplinafiltro, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        disciplinas = paginator.page(page)
    except (EmptyPage, InvalidPage):
        disciplinas = paginator.page(paginator.num_pages)
    return render(request,"core/professor_disciplinas.html",{'disciplinas':disciplinas})

@is_professor()
@login_required
def criar_disciplina(request):
    form = DisciplinaForms(request.POST or None)

    if form.is_valid():
        form = form.save(commit=False)
        form.creator = request.user
        form.save()
        return redirect(reverse('Professor_disciplina'))
    return render(request,"core/criar_disciplinas.html",{'form':form})

@is_professor()
@login_required
def update_disciplina(request,pk):
    disciplina = Disciplina.objects.get(pk=pk)
    form = DisciplinaForms(request.POST or None, instance=disciplina)
    if form.is_valid():
        form = form.save(commit=False)
        form.creator = request.user
        form.save()
        return redirect(reverse('Professor_disciplina'))
    return render(request,"core/criar_disciplinas.html",{'object':disciplina,'form':form})

def delete_disciplina(request,pk):
    disciplina = Disciplina.objects.get(pk=pk)

    if request.method == 'POST':
        form = DisciplinaForms(request.POST or None,instance=disciplina)
        disciplina.delete()
        return redirect(reverse('Professor_disciplina'))
    return render(request,"core/deletar_disciplinas.html",{'object':disciplina})
