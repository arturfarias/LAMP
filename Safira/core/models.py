from django.db import models
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import Permission
from django.db.models.signals import post_save


class Professor(models.Model):
    """ Class responsible for storing teacher data
    """
    class Meta:
        permissions = (("view_professor", 'can_view_professor'),)

    usuario = models.OneToOneField(User, verbose_name="Usuário")
    nome = models.CharField('Nome', max_length=50)
    email = models.EmailField('E-mail')
    sobre = models.CharField('Sobre', max_length=120)

    def __str__(self):
        return self.nome


class Aluno(models.Model):
    """ Class responsible for storing student data
    """
    class Meta:
        permissions = (("view_aluno", 'can_view_aluno'),)

    usuario = models.OneToOneField(User, verbose_name="Usuário")
    nome = models.CharField('Nome', max_length=50)
    email = models.EmailField('E-mail')
    matricula = models.CharField('Matricula', max_length=8)
    sobre = models.CharField('Sobre', max_length=120)

    def __str__(self):
        return self.nome or str(self.usuario)


class Disciplina(models.Model):
    """ Class responsible for storing the data related to the disciplines
    """
    nome = models.CharField('Nome', max_length=50)
    descricao = models.TextField('Descrição')
    creator = models.ForeignKey(User, verbose_name="Criador", blank=True)

    def __str__(self):
        return self.nome


class Turma(models.Model):
    """ Class responsible for storing class data
    """
    nome = models.CharField('Nome', max_length=50)
    professor = models.ForeignKey('Professor', verbose_name="Professor")
    disciplina = models.ForeignKey('Disciplina', verbose_name="Disciplina")
    semestre = models.CharField('Semestre', max_length=7)
    aluno = models.ManyToManyField('Aluno', through='AlunosMatriculados',
                                   blank=True)

    class Meta:
        unique_together = (("nome", "disciplina", "semestre"),)

    def __str__(self):
        return "Turma: " + self.nome + " " + "(" + self.disciplina.nome + ")"


class AlunosMatriculados(models.Model):
    """ Class responsible for storing data pertaining to many-to-many
    relationship between students and classes
    """
    aluno = models.ForeignKey('Aluno', verbose_name="Aluno")
    turma = models.ForeignKey('Turma', verbose_name="Turma")
    pendencia = models.BooleanField('Falta Aprovação', default=True)

    class Meta:
        unique_together = (("aluno", "turma"),)

    def __str__(self):
        return "Aluno: " + self.aluno.nome + " " + "(" + self.turma.nome + ")"


@receiver(pre_save, sender=Aluno)
def handler_permissao_aluno(sender, instance, **kwargs):
    """ Whenever a student and created assigns some permissions to the same
    """
    permission = Permission.objects.get(codename='view_aluno')
    User = instance.usuario
    User.user_permissions.add(permission)


@receiver(pre_save, sender=Professor)
def handler_permissao_professor(sender, instance, **kwargs):
    """ Whenever a teacher is created assign some permissions to the same
    """
    permission = Permission.objects.get(codename='view_professor')
    user = instance.usuario
    user.user_permissions.add(permission)


@receiver(post_save, sender=User)
def cria_user_aluno(sender, instance, created, **kwargs):
    """ Create a student instance for each registered user
    """
    if created:
        if instance.is_staff:
            pass
        else:
            Aluno.objects.create(usuario=instance, email=instance.email)
