from django.conf.urls import include, url
from ..config.views import *

urlpatterns = [
    url(r'^$', index,name='index'),
    url(r'^home$', home, name='home'),
]
