# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-30 20:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, verbose_name='Nome')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('matricula', models.CharField(max_length=8, verbose_name='Matricula')),
                ('sobre', models.CharField(max_length=120, verbose_name='Sobre')),
            ],
            options={
                'permissions': (('view_aluno', 'can_view_aluno'),),
            },
        ),
        migrations.CreateModel(
            name='AlunosMatriculados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pendencia', models.BooleanField(default=True, verbose_name='Falta Aprovação')),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Aluno', verbose_name='Aluno')),
            ],
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, verbose_name='Nome')),
                ('descricao', models.TextField(verbose_name='Descrição')),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Criador')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, verbose_name='Nome')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('sobre', models.CharField(max_length=120, verbose_name='Sobre')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'permissions': (('view_professor', 'can_view_professor'),),
            },
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, verbose_name='Nome')),
                ('semestre', models.CharField(max_length=7, verbose_name='Semestre')),
                ('disciplina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Disciplina', verbose_name='Disciplina')),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Professor', verbose_name='Professor')),
            ],
        ),
        migrations.AddField(
            model_name='alunosmatriculados',
            name='turma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Turma', verbose_name='Turma'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='turma',
            field=models.ManyToManyField(blank=True, through='core.AlunosMatriculados', to='core.Turma'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
        migrations.AlterUniqueTogether(
            name='turma',
            unique_together=set([('nome', 'disciplina', 'semestre')]),
        ),
        migrations.AlterUniqueTogether(
            name='alunosmatriculados',
            unique_together=set([('aluno', 'turma')]),
        ),
    ]
