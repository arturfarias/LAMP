from django.contrib import admin

from django.contrib import admin
from core.ava.models import *

class adminAluno(admin.ModelAdmin):
    model=Aluno


class AdminAlunoDisciplina(admin.ModelAdmin):

    model = AlunoDisciplina

class AdminProfessor(admin.ModelAdmin):
    model=Professor


class AdminDisciplina(admin.ModelAdmin):
    model=Disciplina

class AdminAtividade(admin.ModelAdmin):
    model=Atividades

admin.site.register(Professor,AdminProfessor)
admin.site.register(Disciplina,AdminDisciplina)
admin.site.register(Aluno,adminAluno)
admin.site.register(AlunoDisciplina,AdminAlunoDisciplina)
admin.site.register(Atividades,AdminAtividade)
