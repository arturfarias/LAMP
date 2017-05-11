from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import AlunosMatriculados, Disciplina, Turma, Aluno


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Nome')
    email = forms.EmailField(label='E-mail')

    class Meta:
        model = User
        fields = ['username', 'email']


class MatriculaForm(forms.ModelForm):

    class Meta:
        model = AlunosMatriculados
        fields = ()


class DisciplinaForms(forms.ModelForm):
    class Meta:
        model = Disciplina
        exclude = ['creator']


class Turmaforms(forms.ModelForm):
    class Meta:
        model = Turma
        exclude = ['professor', 'aluno']


class ResetForms(forms.Form):
    user = forms.CharField(label='Nome de Usuario', max_length=50)
    email = forms.EmailField(label='E-mail')
    matricula = forms.CharField(label='Numero de Matricula', max_length=8)

    def clean_user(self):
        user = self.cleaned_data['user']
        if User.objects.filter(username=user).exists():
            return user
        raise forms.ValidationError('Nenhum usuario encontrado')

    def clean_email(self):
        try:
            user = User.objects.get(username=self.cleaned_data['user'])
        except KeyError:
            raise forms.ValidationError('Nenhum E-mail encontrado')
        aluno = Aluno.objects.get(usuario=user.id)
        email = self.cleaned_data['email']
        if email == aluno.email:
            return email
        raise forms.ValidationError('Nenhum E-mail encontrado')

    def clean_matricula(self):
        try:
            user = User.objects.get(username=self.cleaned_data['user'])
        except KeyError:
            raise forms.ValidationError('Nenhuma matricula encontrada')
        aluno = Aluno.objects.get(usuario=user.id)
        matricula = self.cleaned_data['matricula']
        if matricula == aluno.matricula:
            return matricula
        raise forms.ValidationError('Nenhuma matricula encontrada')
