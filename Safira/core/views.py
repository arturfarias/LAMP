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
    """ Homepage, also responsible for login
    """
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
    """ Views Responsible for redirecting the logged in user to his
    corresponding page (Teacher and student for different pages with their
    different characteristics)
    """

    # Check which type of user is pointing you to the correct page
    if request.user.is_staff:  #
        return HttpResponseRedirect("/admin/")
    elif request.user.has_perm('core.view_professor'):
        return redirect(reverse('professor'))
    elif request.user.has_perm('core.view_aluno'):
        return redirect(reverse('aluno'))


def register(request):
    """ Responsible for registering new system users
    """
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
    """ Views for the student page, this page does not render anything, only
     redirects to a new page which will be seen by the student, and used
     because in the future can be sent new data to the student (also simplifies
     the student's initial page exchange)
    """

    return redirect(reverse('Aluno_disciplina'))


@is_professor()
@login_required
def professor(request):
    """ Views to the teacher's page, this page does not render anything, only
    redirects to a new page which will be seen by the teacher, and used because
    in the future can be sent new data to the student (also simplifies the
    student's initial page exchange)
    """

    return redirect(reverse('Professor_disciplina'))


@is_aluno()
@login_required
def Aluno_disciplina(request):
    """ Views that shows the disciplines that the student was accepted
    """
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
    """ Shows all disciplines (and their classes) for the student, also allows
    the student to apply to enroll in a discipline
    """

    # Part listing disciplines and classes for the student
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

    # Party responsible for requesting student's enrollment
    if request.method == 'POST':
        form = MatriculaForm(request.POST)
        form = form.save(commit=False)
        form.aluno = aluno
        form.turma = Turma.objects.get(id=request.POST.get("id_turma"))
        try:
            form.save()
        except IntegrityError:
            pass

    context = {'dis': dis, 'turmas': turmas, 'matriculados': turmas2}

    return render(request, TEMPLATE, context)


@is_professor()
@login_required
def Professor_disciplina(request):
    """ Responsible for listing all teacher's courses logged into the system
    """
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
    """ Create a new discipline and assign it to the teacher who created it
    """
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
    """ Form to edit a discipline (The teacher can only edit their disciplines
    and is not able to change the discipline of the owner)
    """
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
    """ Used to delete a course displaying a confirmation page
    """
    TEMPLATE = "core/deletar_disciplinas.html"
    disciplina = Disciplina.objects.get(pk=pk)

    if request.method == 'POST':
        disciplina.delete()
        return redirect(reverse('Professor_disciplina'))

    return render(request, TEMPLATE, {'object': disciplina})


@is_professor()
@login_required
def professor_turma(request):
    """ Views that lists all classes of a teacher logged into the system
    """
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
    """ Allows the teacher to create a new class for him
    """
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
    """  Form to edit a class (The teacher can only edit their class
    and is not able to change the class of the owner)
    """
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
    """ Used to exclude a class by displaying a confirmation page
    """
    TEMPLATE = "core/deletar_turmas.html"
    turma = Turma.objects.get(pk=pk)

    if request.method == 'POST':
        turma.delete()
        return redirect(reverse('professor_turma'))
    return render(request, TEMPLATE, {'object': turma})


def ver_turmas(request, pk):
    """ Show details of a selected class, such as enrolled students or
    enrollment requests, also allows you to accept or decline requests and
    remove students from the class
    """
    TEMPLATE = "core/ver_turmas.html"
    # Lists all students enrolled in the class
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
        if "aceitar" in request.POST:  # Accepts a student request
            id = request.POST.get("aceitar")
            aluno = AlunosMatriculados.objects.get(id=id)
            form = MatriculaForm(request.POST or None, instance=aluno)
            form = form.save(commit=False)
            form.pendencia = False
            form.save()
        else:
            id = request.POST.get("recusar")  # Deny student application
            aluno = AlunosMatriculados.objects.get(id=id)
            form = MatriculaForm(request.POST or None, instance=aluno)
            aluno.delete()
    # List requests sent by students
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
    """ Used to remove students from a class with a confirmation page
    """
    TEMPLATE = "core/deletar_aluno.html"
    matricula = AlunosMatriculados.objects.get(pk=pk)

    if request.method == 'POST':
        matricula.delete()
        return redirect(reverse('professor_turma'))
    return render(request, TEMPLATE, {'matricula': matricula})


def passwordReset(request):
    """ Displays a form to prove that the student who forgot the password and
    himself, if it is validated leads to a page to define a new password
    IN DEVELOPMENT
    """
    TEMPLATE = "core/reset.html"
    if request.method == 'POST':
        form = ResetForms(request.POST)
        if form.is_valid():
            pass
    else:
        form = ResetForms()
    return render(request, TEMPLATE, {"form": form})
