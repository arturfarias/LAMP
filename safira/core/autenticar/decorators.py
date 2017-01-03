from functools import wraps
from django.http.response import Http404

# Decorator serve como validador de view, ele faz verificacoes que podem proibir ou nao a execucao de uma pagina.
def matriculado(view):
    @wraps(view)
    def wrapp(request,*args,**kwargs):
        aluno=request.user.aluno
        disciplina=kwargs['slug_disc']
        atividade=kwargs['slug']
        try:
            Atividades.objects.get(slug=atividade,disciplina__slug=disciplina)
            aluno.alunodisciplina_set.get(disciplina__slug=disciplina)
        except:
            raise Http404
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
