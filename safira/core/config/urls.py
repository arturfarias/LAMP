from django.conf.urls import include, url
from core.config.views import *

urlpatterns = [
    url(r'^$', index,name='index'),
    url(r'^home$', home, name='home'),
]
