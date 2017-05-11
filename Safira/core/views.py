from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from .forms import RegisterForm, MatriculaForm, DisciplinaForms, Turmaforms
from .forms import ResetForms
from .decorators import is_aluno, is_professor
from .models import AlunosMatriculados, Aluno, Disciplina, Turma, Professor


def index(request):
    TEMPLATE = "core/index.html"
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, TEMPLATE, {"form": form})

    return render(request, TEMPLATE, {"form": AuthenticationForm()})


@login_required
def home(request):
    if request.user.is_staff:
        return HttpResponseRedirect("/admin/")
    elif request.user.has_perm('core.view_professor'):
        return redirect(reverse('professor'))
    elif request.user.has_perm('core.view_aluno'):
        return redirect(reverse('aluno'))


def register(request):
    TEMPLATE = "core/register.html"
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegisterForm()

    return render(request, TEMPLATE, {"form": form})


@is_aluno()
@login_required
def aluno(request):

    return redirect(reverse('Aluno_disciplina'))


@is_professor()
@login_required
def professor(request):

    return redirect(reverse('Professor_disciplina'))


@is_aluno()
@login_required
def Aluno_disciplina(request):
    TEMPLATE = "core/minhas_disciplinas.html"
    aluno = Aluno.objects.get(usuario=request.user)
    matriculados = AlunosMatriculados
    filtro = matriculados.objects.filter(aluno_id=aluno,
                                         pendencia=False).order_by('turma')
    paginator = Paginator(filtro, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        disciplinas = paginator.page(page)
    except (EmptyPage, InvalidPage):
        disciplinas = paginator.page(paginator.num_pages)

    return render(request, TEMPLATE, {'disciplinas': disciplinas})


@is_aluno()
@login_required
def All_disciplinas(request):
    TEMPLATE = "core/disciplinas.html"
    aluno = Aluno.objects.get(usuario=request.user)
    lista_disciplinas = Disciplina.objects.all().order_by('nome')
    turmas = Turma.objects.all()
    turmas2 = Turma.objects.all().order_by('semestre').exclude(aluno=aluno)

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
        try:
            form.save()
        except IntegrityError:
            pass  # futuramente colocar uma mansagem de erro

    context = {'dis': dis, 'turmas': turmas, 'matriculados': turmas2}

    return render(request, TEMPLATE, context)


@is_professor()
@login_required
def Professor_disciplina(request):
    TEMPLATE = "core/professor_disciplinas.html"
    filtro = Disciplina.objects.filter(creator=request.user).order_by('nome')
    paginator = Paginator(filtro, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        disciplinas = paginator.page(page)
    except (EmptyPage, InvalidPage):
        disciplinas = paginator.page(paginator.num_pages)

    return render(request, TEMPLATE, {'disciplinas': disciplinas})


@is_professor()
@login_required
def criar_disciplina(request):
    TEMPLATE = "core/criar_disciplinas.html"
    form = DisciplinaForms(request.POST or None)

    if form.is_valid():
        form = form.save(commit=False)
        form.creator = request.user
        form.save()
        return redirect(reverse('Professor_disciplina'))

    return render(request, TEMPLATE, {'form': form})


@is_professor()
@login_required
def update_disciplina(request, pk):
    TEMPLATE = "core/criar_disciplinas.html"
    disciplina = Disciplina.objects.get(pk=pk)
    form = DisciplinaForms(request.POST or None, instance=disciplina)
    if form.is_valid():
        form = form.save(commit=False)
        form.creator = request.user
        form.save()
        return redirect(reverse('Professor_disciplina'))

    context = {'object': disciplina,
               'form': form}

    return render(request, TEMPLATE, context)


@is_professor()
@login_required
def delete_disciplina(request, pk):
    TEMPLATE = "core/deletar_disciplinas.html"
    disciplina = Disciplina.objects.get(pk=pk)

    if request.method == 'POST':
        disciplina.delete()
        return redirect(reverse('Professor_disciplina'))

    return render(request, TEMPLATE, {'object': disciplina})


@is_professor()
@login_required
def professor_turma(request):
    TEMPLATE = "core/professor_turmas.html"
    professor = Professor.objects.get(usuario=request.user)
    turmas = Turma.objects.filter(professor_id=professor).order_by('nome')
    paginator = Paginator(turmas, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        turmas = paginator.page(page)
    except (EmptyPage, InvalidPage):
        turmas = paginator.page(paginator.num_pages)

    return render(request, TEMPLATE, {'turmas': turmas})


@is_professor()
@login_required
def criar_turma(request):
    TEMPLATE = "core/criar_turma.html"
    form = Turmaforms(request.POST or None)

    if form.is_valid():
        form = form.save(commit=False)
        form.professor = Professor.objects.get(usuario=request.user)
        form.save()
        return redirect(reverse('professor_turma'))

    return render(request, TEMPLATE, {'form': form})


@is_professor()
@login_required
def update_turma(request, pk):
    TEMPLATE = "core/criar_turma.html"
    turma = Turma.objects.get(pk=pk)
    form = Turmaforms(request.POST or None, instance=turma)
    if form.is_valid():
        form = form.save(commit=False)
        form.professor = Professor.objects.get(usuario=request.user)
        form.save()
        return redirect(reverse('professor_turma'))

    context = {'object': turma,
               'form': form}

    return render(request, TEMPLATE, context)


@is_professor()
@login_required
def delete_turma(request, pk):
    TEMPLATE = "core/deletar_turmas.html"
    turma = Turma.objects.get(pk=pk)

    if request.method == 'POST':
        turma.delete()
        return redirect(reverse('professor_turma'))
    return render(request, TEMPLATE, {'object': turma})


def ver_turmas(request, pk):
    TEMPLATE = "core/ver_turmas.html"
    find = AlunosMatriculados.objects.filter(turma=pk,
                                             pendencia=True).order_by('turma')
    paginator = Paginator(find, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        alunossolis = paginator.page(page)
    except (EmptyPage, InvalidPage):
        alunossolis = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        if "aceitar" in request.POST:
            id = request.POST.get("aceitar")
            aluno = AlunosMatriculados.objects.get(id=id)
            form = MatriculaForm(request.POST or None, instance=aluno)
            form = form.save(commit=False)
            form.pendencia = False
            form.save()
        else:
            id = request.POST.get("recusar")
            aluno = AlunosMatriculados.objects.get(id=id)
            form = MatriculaForm(request.POST or None, instance=aluno)
            aluno.delete()

    turma = Turma.objects.get(pk=pk)
    matriculados = AlunosMatriculados
    filtro = matriculados.objects.filter(turma=pk,
                                         pendencia=False).order_by('turma')
    paginator = Paginator(filtro, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        alunos = paginator.page(page)
    except (EmptyPage, InvalidPage):
        alunos = paginator.page(paginator.num_pages)

    context = {'turma': turma,
               'alunos': alunos,
               'alunossolis': alunossolis}

    return render(request, TEMPLATE, context)


@is_professor()
@login_required
def delete_Aluno(request, pk):
    TEMPLATE = "core/deletar_aluno.html"
    matricula = AlunosMatriculados.objects.get(pk=pk)

    if request.method == 'POST':
        matricula.delete()
        return redirect(reverse('professor_turma'))
    return render(request, TEMPLATE, {'matricula': matricula})


def passwordReset(request):
    TEMPLATE = "core/reset.html"
    if request.method == 'POST':
        form = ResetForms(request.POST)
        if form.is_valid():
            pass
    else:
        form = ResetForms()
    return render(request, TEMPLATE, {"form": form})
