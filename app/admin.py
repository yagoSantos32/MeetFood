# seu_app/admin.py

from django.contrib import admin
from .models import Cidade, Usuario, Doacao, Solicitacao, Mensagem, Avaliacao, Estoque, Relatorio

admin.site.register(Cidade)
admin.site.register(Usuario)
admin.site.register(Doacao)
admin.site.register(Solicitacao)
admin.site.register(Mensagem)
admin.site.register(Avaliacao)
admin.site.register(Estoque)
admin.site.register(Relatorio)
