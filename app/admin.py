from django.contrib import admin
from .models import Cidade, Usuario, Doacao, Solicitacao, Mensagem, Avaliacao


@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'uf')
    search_fields = ('nome', 'uf')


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'tipo_usuario', 'cidade')
    list_filter = ('tipo_usuario', 'cidade')
    search_fields = ('nome', 'email', 'cpf_cnpj')


@admin.register(Doacao)
class DoacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'restaurante', 'status', 'data')
    list_filter = ('status',)
    search_fields = ('titulo', 'descricao')


@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ('instituicao', 'doacao', 'status', 'data')
    list_filter = ('status',)
    search_fields = ('mensagem',)


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('remetente', 'destinatario', 'timestamp')
    search_fields = ('texto',)


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('avaliador', 'avaliado', 'nota', 'data')
    list_filter = ('nota',)
    search_fields = ('comentario',)
