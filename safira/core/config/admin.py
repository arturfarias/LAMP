from django.contrib import admin

from core.config.models import *


class RodapeInline(admin.StackedInline):
    model = Rodape
    fieldsets =[ ('Rodape',{'fields':['icone','texto','link'],'classes':['collapse']}),]
class AdminConfigSistema(admin.ModelAdmin):

    model=Configuracoes_Sistema
    inlines = [RodapeInline,]

class AdminRodapeSistema(admin.ModelAdmin):
    model=Rodape



admin.site.register(Configuracoes_Sistema,AdminConfigSistema)
#admin.site.register(Rodape,AdminRodapeSistema)
