from django.db import models
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import Permission

class Professor(models.Model):
    class Meta:
        permissions=(("view_professor",'can_view_professor'),)

    usuario = models.OneToOneField(User,verbose_name="Usuário")
    nome = models.CharField('Nome',max_length=50)
    email = models.EmailField('E-mail')
    sobre = models.CharField('Sobre',max_length=120)

    def __str__(self):
        return self.nome

class Aluno(models.Model):
    class Meta:
        permissions=(("view_aluno",'can_view_aluno'),)

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
    professor = models.ForeignKey('Professor',verbose_name="Professor")
    disciplina = models.ForeignKey('Disciplina',verbose_name="Disciplina")
    semestre = models.CharField('Semestre',max_length=7)

    def __str__(self):
        return "Turma: " + self.nome + " " +  "(" + self.disciplina.nome + ")"

class AlunosMatriculados(models.Model):
    aluno = models.ForeignKey('Aluno',verbose_name="Aluno")
    turma = models.ForeignKey('Turma',verbose_name="Turma")
    semestre = models.CharField('Semestre',max_length=7)
    class Meta:
        unique_together = (("aluno", "turma","semestre"),)

    def __str__(self):
        return "Aluno: " + self.aluno.nome + " " +  "(" + self.turma.nome + ")"

@receiver(pre_save,sender=Aluno)
def handler_permissao_aluno(sender,instance,**kwargs):
    permission = Permission.objects.get(codename='view_aluno')
    User=instance.usuario
    User.user_permissions.add(permission)

@receiver(pre_save,sender=Professor)
def handler_permissao_professor(sender,instance,**kwargs):
    permission = Permission.objects.get(codename='view_professor')
    user=instance.usuario
    user.user_permissions.add(permission)
