# # -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch.dispatcher import receiver
from django.db.models.signals import m2m_changed,post_save, pre_save, pre_init
from .validators import *


## Elementos de Configuração do Sistema ##
class Configuracoes_Sistema(models.Model):
    bloquear_criacao=models.BooleanField(default=True,unique=True,editable=False)
    titulo_pagInicial=models.CharField(default="Texto Padrão",max_length=30)
    subTitulo_pagInicial=models.CharField(default="Altere-o através da interface de ADMIN",max_length=40)
    elementos_rodape=models.IntegerField(default=10,max_length=2,validators=[validar_quantidadeElementosRodape])
    icone=models.ImageField(blank=True,upload_to="imagens/icone")


class Rodape(models.Model):
    icone=models.ImageField(blank=True,upload_to="imagens/rodape/icone",help_text="Coloque o icone no tamanho y x y")
    texto=models.CharField(blank=False,help_text="Texto que vai aparecer no icone",max_length=30)
    link=models.URLField(blank=True,help_text="Coloque um link para redirecionar para a página")
    configuracoes_Sistema=models.ForeignKey(Configuracoes_Sistema)

    def __unicode__(self):
        return self.texto

#Coloca automaticamente a permissao de aluno, toda vez que um aluno é criado
@receiver(pre_save,sender=Rodape)
def handler_Rodape(sender,instance,**kwargs):
    try:
        if Rodape.objects.get(pk=instance.pk):
            pass
    except:
        if len(Rodape.objects.filter())>=instance.configuracoes_Sistema.elementos_rodape:
            raise ValidationError("Você inseriu mais elementos que o configurado, altere a quantidade ou remova algum elemento do rodapé para continuar inserindo!")
