from django.shortcuts import  render, redirect
from django.http import HttpResponse,HttpResponseRedirect

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

def index(request):
    if  request.user.is_authenticated(): # Redireciona a central caso ja esteja lo
        return redirect(central)
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): # verifica se e valido
            login(request, form.get_user())
            return HttpResponseRedirect("/central/")
        else:
            return render(request, "index.html", {"form": form})
    return render(request, "index.html", {"form": AuthenticationForm()})

def central(request):
    return HttpResponse("Bem vindo a essa linda pagina em branco.")
# Create your views here.
