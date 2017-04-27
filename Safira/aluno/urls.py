from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'safira/aluno/$', views.aluno, name='aluno'), #pagina que vai ao logar
]
