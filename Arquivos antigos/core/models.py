from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,UserManager

#Classe para criar um usuário personalizado no django
class User(AbstractBaseUser,PermissionsMixin):

    username = models.CharField('Nome de Usuário',max_length=30,unique=True)
    email = models.EmailField('E-mail',unique=True)
    name = models.CharField('Nome',max_length=100,blank=True)
    is_active = models.BooleanField('Está Ativo?',blank=True,default=True)
    is_staff = models.BooleanField('É da Equipe?',blank=True,default=False)
    date_joined = models.DateTimeField('Data de Entrada',auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name or self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return str(self)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

#Classe para o usuário do tipo Professor
class Professor(models.Model):
    nome = models.CharField('Nome',max_length=100)
    email = models.EmailField('E-mail')
    user = models.ForeignKey(User,verbose_name='Usuário')

    def __str__(self):
        return self.nome

class Aluno(models.Model):
    nome = models.CharField('Nome',max_length=100)
    email = models.EmailField('E-mail')
    user = models.ForeignKey(User,verbose_name='Usuário')

    def __str__(self):
        return self.nom
