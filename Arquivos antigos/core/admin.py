from django.contrib import admin
from .models import User,Professor,Aluno

admin.site.register(User)
admin.site.register(Professor)
admin.site.register(Aluno)
# Register your models here.