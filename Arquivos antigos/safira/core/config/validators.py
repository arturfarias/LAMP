from django.core.exceptions import ValidationError


#Aqui são encontrados todas as funções de validação de dados para as models


#Valida a quantidade de elementos no rodapé do Site, visando limitar a uma quantidade rasoavel
def validar_quantidadeElementosRodape(value):
    if value >10:
        raise ValidationError("A quantidade maxima de elementos no rodape é 10!")

def valida_QuantidadeRodape(value):

    if len(Rodape.objects.filter(configuracoes_Sistema=1)) > Configuracoes_Sistema.objects.get(pk=1).elementos_rodape:

        raise ValidationError("Você inseriu mais elementos que o configurado, altere a quantidade ou remova algum elemento do rodapé para continuar inserindo!")
