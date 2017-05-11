from django.contrib import admin
from .models import Professor, Aluno, Disciplina, Turma, AlunosMatriculados

admin.site.register(Professor)
admin.site.register(Aluno)
admin.site.register(Disciplina)
admin.site.register(Turma)
admin.site.register(AlunosMatriculados)
