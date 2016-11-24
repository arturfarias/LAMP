# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(help_text=b'Escreva o seu nome completo', max_length=50)),
                ('orientador', models.CharField(max_length=50, blank=True)),
                ('email_orientador', models.EmailField(max_length=75, blank=True)),
                ('chave_de_ativacao', models.CharField(max_length=40, null=True, blank=True)),
                ('chave_expira', models.DateTimeField(default=datetime.datetime(2015, 6, 19, 12, 37, 4, 922988), blank=True)),
            ],
            options={
                'permissions': (('view_aluno', 'can_view_aluno'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AlunoDisciplina',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(help_text=b'nome bonito para as urls', unique=True, max_length=100, blank=True)),
                ('pendencia', models.BooleanField(default=True, help_text=b'True = Pendente a aprova\xc3\xa7\xc3\xa3o e False = Aceito na disciplina', verbose_name=b'Pendente')),
                ('aluno', models.ForeignKey(to='ava.Aluno')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Atividades',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=100, blank=True)),
                ('titulo', models.CharField(max_length=30)),
                ('arquivo', models.FileField(upload_to=b'atividades/arquivos/atividades')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=100, blank=True)),
                ('nome', models.CharField(max_length=50)),
                ('semestre', models.CharField(help_text=b'Ex: 2014.1', max_length=20)),
                ('data_criacao', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=75)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_professor', 'can_view_professor'),),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='disciplina',
            name='professor',
            field=models.ForeignKey(to='ava.Professor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='atividades',
            name='disciplina',
            field=models.ForeignKey(to='ava.Disciplina'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alunodisciplina',
            name='disciplina',
            field=models.ForeignKey(to='ava.Disciplina'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='alunodisciplina',
            unique_together=set([('aluno', 'disciplina')]),
        ),
        migrations.AddField(
            model_name='aluno',
            name='disciplinas',
            field=models.ManyToManyField(to='ava.Disciplina', through='ava.AlunoDisciplina', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aluno',
            name='usuario',
            field=models.OneToOneField(verbose_name=b'Usu\xc3\xa1rio/Email', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
