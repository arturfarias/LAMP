# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from ..ava.decorators import is_professor
from ..ava.forms import RegistrarAluno
from ..ava.models import AlunoDisciplina

#Chama a pagina index, que possui dois formulario, o de login e o de cadastro.
def index(request,sucesso=2):
    return render(request, 'index.html',{'form_login':AuthenticationForm(request.POST or None),'form':RegistrarAluno(request.POST or None),'sucesso':sucesso})

#Chama a home do sistema
@login_required
def home(request):
    dados={}
    if request.user.has_perm('admin'):
        return render(request, 'Template_Error.html',{'mensagem':"Você não possui permissão para Logar no sistema",'titulo':'Aviso!'})
    if request.user.has_perm('ava.view_professor'):
        return redirect(reverse(viewname='home_professor'))
    elif request.user.has_perm('ava.view_aluno'):
        return redirect(reverse(viewname='home_aluno'))
