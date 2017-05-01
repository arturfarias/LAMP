from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views

urlpatterns = [
    url(r'safira/$', views.index, name='index'), # pagina principal e de login
    url(r'safira/home/$', views.home, name='home'), #pagina que vai ao logar
    url(r'register/$', views.register, name='register'), # pagina principal e de login
    url(r'^sair/$', logout,{'next_page':'index'},name='logout'),
    url(r'safira/aluno/$', views.Aluno_disciplina, name='Aluno_disciplina'),
    url(r'safira/professor/$', views.Professor_disciplina, name='Professor_disciplina'),
    url(r'safira/aluno/disciplinas/$', views.All_disciplinas, name='All_disciplinas'),
    url(r'safira/professor/criar/$', views.criar_disciplina, name='criar_disciplina'),
    url(r'safira/professor/editar/(?P<pk>\d+)/$', views.update_disciplina, name='update_disciplina'),
    url(r'safira/professor/deletar(?P<pk>\d+)/$', views.delete_disciplina, name='delete_disciplina'),
]
