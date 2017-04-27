from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'safira/professor/$', views.professor, name='professor'), #pagina que vai ao logar
]
