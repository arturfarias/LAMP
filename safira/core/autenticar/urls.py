from django.conf.urls import include, url
from core.autenticar.views import *

urlpatterns = [
    url(r'^mudar_senha$', mudar_senha, name='mudar_senha'),
    url(r'^mudar_senha/concluido/$', 'django.contrib.auth.views.password_change_done',{'template_name':'mudar_senha.html'},name= 'senha_alterada'),
    url(r'^registrar$', registrar,name='registrar'),
    url(r'^login$', logar,name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout',{'next_page':'/'},name='logout'),
    url(r'^ativar/(?P<codigo>\w+)/', ativar_conta,name="ativar_conta"),
]
