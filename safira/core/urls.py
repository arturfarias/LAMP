from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'central/$', views.central, name='central'),
    url(r'cadastrar/$', views.cadastrar, name='cadastrar'),
]
