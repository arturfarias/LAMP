from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.decorators import  is_aluno,is_professor

@is_professor()
@login_required
def professor(request):
    return render(request,"core/professor.html")
