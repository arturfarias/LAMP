#encoding: utf-8
from functools import wraps

from django.http.response import Http404



# Decorator serve como validador de view, ele faz verificacoes que podem proibir ou nao a execucao de uma pagina.
from ..ava.models import Disciplina
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

__author__ = 'allan'


def is_aluno(login_url=None, raise_exception=False):
    perm='ava.view_aluno'

    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_perms(user):
        if not isinstance(perm, (list, tuple)):
            perms = (perm, )
        else:
            perms = perm
        # First check if the user has the permission (even anon users)
        if user.has_perms(perms):
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(check_perms, login_url=login_url)


from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied




def is_professor(login_url=None, raise_exception=False):
    perm='ava.view_professor'

    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_perms(user):
        if not isinstance(perm, (list, tuple)):
            perms = (perm, )
        else:
            perms = perm
        # First check if the user has the permission (even anon users)
        if user.has_perms(perms):
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(check_perms, login_url=login_url)

def matriculado_disc_atividade(view):
    @wraps(view)
    def wrapp(request,*args,**kwargs):
        aluno=request.user.aluno
        disciplina=kwargs['slug_disc']
        atividade=kwargs['slug']
        try:

            pass
        except:
            raise Http404("Permissao negada")
        return view(request, *args,**kwargs)
    return wrapp


def matriculado_disc(view):
    @wraps(view)
    def wrapp(request,*args,**kwargs):
        aluno=request.user.aluno
        disciplina=kwargs['slug']

        try:

            aluno.alunodisciplina_set.get(disciplina__slug=disciplina)
        except:
            raise Http404
        return view(request, *args,**kwargs)
    return wrapp


# Decorator serve como validador de view, ele faz verificacoes que podem proibir ou nao a execucao de uma pagina.
def administrador_disciplina(view):
    @wraps(view)
    def wrapp(request,*args,**kwargs):
        professor=request.user.professor
        disciplina=kwargs['slug']

        try:
            Disciplina.objects.get(slug=disciplina,professor=professor)
        except:
            raise Http404("Você não possui permissão para continuar")
        return view(request, *args,**kwargs)
    return wrapp
