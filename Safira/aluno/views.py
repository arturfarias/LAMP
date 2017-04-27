from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from core.decorators import  is_aluno,is_professor

@is_aluno()
@login_required
def aluno(request):
    return redirect(reverse('Aluno_disciplina'))
