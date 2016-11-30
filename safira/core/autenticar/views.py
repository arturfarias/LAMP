# -*- coding: utf-8 -*-
import hashlib
import random
import datetime

from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http.response import HttpResponseRedirect, HttpResponse

from ..autenticar.forms import RegistrationForm
from ..ava.models import Aluno
from ..config.views import index
from ..ava.forms import RegistrarAluno



@sensitive_post_parameters()
@csrf_protect
@login_required
def mudar_senha(request):

    if request.method == "POST":

        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one if
            # django.contrib.autenticar.middleware.SessionAuthenticationMiddleware
            # is enabled.
            update_session_auth_hash(request, form.user)
            return HttpResponse('Senha alterada com sucesso!')

    return HttpResponseRedirect(reverse(viewname='atualiza_perfil'))



#Dados Username e Password corretos o usurário conseguirá logar normalmente
def logar(request):


    if request.method=='POST':


        form=AuthenticationForm(data=request.POST)

        if form.is_valid():
            login(request,form.get_user())
            return redirect(reverse(viewname='home'))

    return index(request,False)

#Função que cria um novo aluno quando recebe uma requisição post
#Cadastro com Nome, Email e Senha
def registrar(request):

    if request.method=='POST':
        form=RegistrarAluno(request.POST)
        user_form=RegistrationForm(request.POST)
        if form.is_valid() and user_form.is_valid():
            with transaction.atomic():

                user=user_form.save(commit=False)
                aluno=form.save(commit=False)
                user.is_active=False
                user.save()

                #Gerando uma chave para ativar o email
                salt=hashlib.sha1(str(random.random())).hexdigest()[:5]
                activation_key=hashlib.sha1(salt+user.email).hexdigest()
                key_expires=datetime.datetime.now()

                aluno.usuario=user
                aluno.chave_de_ativacao=activation_key
                aluno.chave_expira=key_expires

                #Corpo do Email
                email_assunto="Peer Assesment - Confirmação de cadastro"
                link=reverse(viewname='ativar_conta',kwargs={'codigo':activation_key})
                email_corpo="http://"+request.get_host()+link
                aluno.save()
                send_mail(email_assunto,email_corpo,user.email,[user.email],fail_silently=False)






                return index(request,sucesso=True)


    return index(request,sucesso=False)




def ativar_conta(request,codigo):
    aluno=get_object_or_404(Aluno,chave_de_ativacao=codigo)
    user=aluno.usuario
    if user.is_active == False:
        user.is_active=True
        user.save()
        return HttpResponse("Cadastro confirmado com sucesso!")

    return HttpResponseRedirect('/')
