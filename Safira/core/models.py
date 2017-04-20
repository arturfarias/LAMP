from django.db import models
from django.contrib.auth.models import User

class Professor(models.Model):
    usuario = models.OneToOneField(User,verbose_name="Usuário")
    nome = models.CharField('Nome',max_length=50)
    email = models.EmailField('E-mail')
    sobre = models.CharField('Sobre',max_length=120)

    def __str__(self):
        return self.nome

class Aluno(models.Model):
    usuario = models.OneToOneField(User,verbose_name="Usuário")
    nome = models.CharField('Nome',max_length=50)
    email = models.EmailField('E-mail')
    matricula = models.CharField('Matricula',max_length=8)
    turma=models.ManyToManyField('Turma',through='AlunosMatriculados',blank=True)
    sobre = models.CharField('Sobre',max_length=120)

    def __str__(self):
        return self.nome

class Disciplina(models.Model):
    nome = models.CharField('Nome',max_length=50)
    descricao = models.TextField('Descrição')

    def __str__(self):
        return self.nome

class Turma(models.Model):
    nome = models.CharField('Nome',max_length=50)
    professor = models.ForeignKey(Professor,verbose_name="Professor")
    disciplina = models.ForeignKey(Disciplina,verbose_name="Disciplina")
    semestre = models.CharField('Semestre',max_length=7)

    def __str__(self):
        return "Turma: " + self.nome + " " +  "(" + self.disciplina.nome + ")"

class AlunosMatriculados(models.Model):
    aluno = models.ForeignKey(Aluno,verbose_name="Aluno")
    Turma = models.ForeignKey(Turma,verbose_name="Turma")

    def __str__(self):
        return "Aluno: " + self.aluno.nome + " " +  "(" + self.Turma.nome + ")"
