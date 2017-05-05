from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views

urlpatterns = [
    url(r'safira/$', views.index, name='index'), # pagina principal e de login
    url(r'safira/home/$', views.home, name='home'), #pagina que vai ao logar
    url(r'register/$', views.register, name='register'), # pagina principal e de login
    url(r'^sair/$', logout,{'next_page':'index'},name='logout'),
    url(r'safira/homeAluno/$', views.aluno, name='aluno'),
    url(r'safira/aluno/$', views.Aluno_disciplina, name='Aluno_disciplina'),
    url(r'safira/homeProfessor/$', views.professor, name='professor'),
    url(r'safira/professor/$', views.Professor_disciplina, name='Professor_disciplina'),
    url(r'safira/aluno/disciplinas/$', views.All_disciplinas, name='All_disciplinas'),
    url(r'safira/professor/turmas/$', views.professor_turma, name='professor_turma'),
    url(r'safira/professor/turma/criar/$', views.criar_turma, name='criar_turma'),
    url(r'safira/professor/criar/$', views.criar_disciplina, name='criar_disciplina'),
    url(r'safira/professor/editar/(?P<pk>\d+)/$', views.update_disciplina, name='update_disciplina'),
    url(r'safira/professor/turma/editar/(?P<pk>\d+)/$', views.update_turma, name='update_turma'),
    url(r'safira/professor/deletar/disciplina/(?P<pk>\d+)/$', views.delete_disciplina, name='delete_disciplina'),
    url(r'safira/professor/turma/deletar/(?P<pk>\d+)/$', views.delete_turma, name='delete_turma'),
    url(r'safira/professor/turma/ver/(?P<pk>\d+)/$', views.ver_turmas, name='ver_turmas'),
    url(r'safira/professor/aluno/deletar/(?P<pk>\d+)/$', views.delete_Aluno, name='delete_aluno'),
]
