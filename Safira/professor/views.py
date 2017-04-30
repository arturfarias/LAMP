from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from core.decorators import  is_aluno,is_professor

@is_professor()
@login_required
def professor(request):
    return redirect(reverse('Professor_disciplina'))
