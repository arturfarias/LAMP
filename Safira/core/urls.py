from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views

urlpatterns = [
    url(r'safira/$', views.index, name='index'), # pagina principal e de login
    url(r'safira/home/$', views.home, name='home'), #pagina que vai ao logar
    url(r'register/$', views.register, name='register'), # pagina principal e de login
]
