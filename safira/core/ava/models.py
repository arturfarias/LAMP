#encoding: utf-8
import os
from django.utils import timezone

__author__ = 'allan'

from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, pre_delete
from django.utils.text import slugify
from django.contrib.auth.models import Permission
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver
from ..autenticar.models import User

#Modelo do professor, contendo todos os seus atributos
class Professor(models.Model):
    class Meta:
        permissions=(("view_professor",'can_view_professor'),)
    nome=models.CharField(max_length=50,blank=False)
    email=models.EmailField(blank=False)
    user= models.OneToOneField(User)
    def __str__(self):
        return self.nome

#Modelo de aluno, contendo seus atributos e sua permissão.
class Aluno(models.Model):
    class Meta:
        permissions=(("view_aluno",'can_view_aluno'),)

    nome=models.CharField(max_length=50,help_text='Escreva o seu nome completo')

    orientador=models.CharField(max_length=50,blank=True)
    email_orientador=models.EmailField(blank=True)
    disciplinas=models.ManyToManyField('Disciplina',through='AlunoDisciplina',blank=True)
    usuario=models.OneToOneField(User,verbose_name="Usuário/Email",)
    chave_de_ativacao=models.CharField(max_length=40,blank=True,null=True)
    chave_expira=models.DateTimeField(default=timezone.now(),blank=True)

    def __str__(self):

        return self.nome

#Modelo para relacionar aluno com disciplina.
class AlunoDisciplina(models.Model):
    slug=models.SlugField(help_text="nome bonito para as urls",blank=True,max_length=100,unique=True,db_index=True)
    disciplina=models.ForeignKey('Disciplina')
    aluno=models.ForeignKey(Aluno)
    pendencia=models.BooleanField(help_text="True = Pendente a aprovação e False = Aceito na disciplina",default=True,verbose_name="Pendente")

    class Meta:
        unique_together=('aluno','disciplina',)
    def format_slug(self):
        return self.aluno.nome +'-'+self.disciplina.nome
    #Função para realizar solicitação e não correr em problemas posteriormente.
    def save_securit(self):
        if AlunoDisciplina.objects.filter(aluno=self.aluno,disciplina=self.disciplina):
            return "Você já realizou uma solicitação,aguarde aprovação."
        else:
            self.save()
            return "Solicitação realizada com sucesso, aguarde aprovação."

    def __str__(self):
        return "[Disciplina]: %s , [Aluno]: %s"%(self.disciplina,self.aluno)
    #retorna uma url redirecionando para o detalhe da disciplina
    def get_absolute_url(self):
        return reverse(viewname='detalhe_disciplinas',kwargs={'slug':self.slug})

## Atividades ##

class Atividades(models.Model):
    slug=models.SlugField(max_length=100,blank=True,unique=True,db_index=True)
    titulo=models.CharField(max_length=30)
    arquivo=models.FileField(upload_to='atividades/arquivos/atividades')
    disciplina=models.ForeignKey('Disciplina')

#Disciplinas#

class Disciplina(models.Model):
    slug=models.SlugField(blank=True,max_length=100,unique=True,db_index=True)
    professor=models.ForeignKey(Professor)
    nome=models.CharField(max_length=50)
    semestre=models.CharField(help_text="Ex: 2014.1",max_length=20,choices=())
    data_criacao=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


##  ALUNO  ##

#signals ou trigers

#Trigger para criação automatica do slug da disciplina

@receiver(pre_save,sender=AlunoDisciplina)
def handler_aluno_disciplina(sender,instance,**kwargs):
    if not instance.slug:
        url=slugify(instance.disciplina.nome+"-"+instance.aluno.nome)
        cont=1
        #Verifica se ja possui nome igual e se possuir acrescenta um valor ao final do nome

        while True:
            try:
                AlunoDisciplina.objects.get(slug=url+"-"+str(cont))
                cont+=1
            except:
                break

        url=slugify(url+"-%s"%cont)

        instance.slug=url


#Coloca automaticamente a permissao de aluno, toda vez que um aluno é criado
@receiver(pre_save,sender=Aluno)
def handler_permissao_aluno(sender,instance,**kwargs):
    permission = Permission.objects.get(codename='view_aluno')
    user=instance.usuario
    user.user_permissions.add(permission)


## Atividades ##

@receiver(pre_save,sender=Atividades)
def handler_slug_atividade(sender,instance,**kwargs):

    if not instance.slug:
        url=slugify(instance.titulo+"-"+instance.disciplina.nome)
        cont=1
        while True:
            try:
                Atividades.objects.get(slug=url+"-"+str(cont))
                cont+=1
            except:
                break

        url=slugify(url+"-%s"%cont)

        instance.slug=url

    try:#Caso a instancia exista ele executara esse codigo
        atvd_armazenada=Atividades.objects.get(pk=instance.pk)

        #Remove o arquivo antigo, antes de adicionar o novo
        if instance.arquivo!=atvd_armazenada.arquivo:
            os.remove(atvd_armazenada.arquivo.path)
    except:
        pass

#deleta o arquivo relacionado a atividade caso ela seja removida
@receiver(pre_delete,sender=Atividades)
def handler_delete_file_atividade(sender,instance,**kwargs):
    instance.arquivo.delete()

## Disciplina ##


#popula automaticamente o slug da disciplina
@receiver(pre_save,sender=Disciplina)
def handler_disciplina(sender,instance,**kwargs):
    if not instance.slug:
        url=slugify(instance.nome+"-"+instance.semestre)
        cont=1
        while True:
            try:
                Disciplina.objects.get(slug=url+"-"+str(cont))
                cont+=1
            except:
                break

        url=slugify(url+"-%s"%cont)

        instance.slug=url


#trigger para antes de salvar o professor no banco, adicionar algumas permissoes ao seu usuario
@receiver(pre_save,sender=Professor)
def handler_permissao_professor(sender,instance,**kwargs):
    permission = Permission.objects.get(codename='view_professor')
    user=instance.user
    user.user_permissions.add(permission)
