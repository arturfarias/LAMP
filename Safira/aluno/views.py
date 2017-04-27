from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.decorators import  is_aluno,is_professor

@is_aluno()
@login_required
def aluno(request):
    return render(request,"core/aluno.html")
