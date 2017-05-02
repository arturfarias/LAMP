from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import AlunosMatriculados,Disciplina,Turma

class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Nome')
    email = forms.EmailField(label='E-mail')
    class Meta:
        model = User
        fields = ['username','email']

class MatriculaForm(forms.ModelForm):

    class Meta:
        model = AlunosMatriculados
        fields = ()

class DisciplinaForms(forms.ModelForm):
    class Meta:
        model = Disciplina
        exclude =['creator']

class Turmaforms(forms.ModelForm):
    class Meta:
        model = Turma
        exclude =['professor']
