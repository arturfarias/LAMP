from django import forms
from django.core.exceptions import ValidationError
from ..ava.models import *
from django.forms.widgets import TextInput


class AtualizarProfessor(forms.ModelForm):
    nome=forms.CharField(widget=TextInput(
        attrs={'class':'form-control'}
    ))

    class Meta:
        model=Professor
        fields=['nome','email']

class RegistrarAluno(forms.ModelForm):
    class Meta:
        model=Aluno
        fields=['nome']

    def clean_nome(self):
        data=self.cleaned_data['nome']
        if data== '':

            raise ValidationError("Nome errado")
        return data

class SolicitaPart(forms.ModelForm):
    class Meta:
        model=AlunoDisciplina
        fields = '__all__'


class AtualizarAluno(forms.ModelForm):
    class Meta:
        model=Aluno
        fields=['nome','orientador','email_orientador']


class FormDisciplina(forms.ModelForm):
    class Meta:
        model=Disciplina
        fields=['nome','semestre']
