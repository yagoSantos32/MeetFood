# config/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app.views import *



urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    path('index/', exemplo_cards, name='index'),
    path('', LoginView.as_view(), name='login'),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('index/', index_view, name='index'),
    path('logout/', logout_view, name='logout'),
    path('chat/', chat_view, name='chat'),
    path('doacoes/', doacoes_view, name='doacoes'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('perfil/editar/', editar_perfil, name='editar_perfil'),




    # Doações
    path('doacoes/minhas/', MinhasDoacoesView.as_view(), name='minhas_doacoes'),

    # Solicitações
    path('solicitacoes/nova/<int:doacao_id>/', SolicitarDoacaoView.as_view(), name='solicitar_doacao'),
    path('solicitacoes/minhas/', MinhasSolicitacoesView.as_view(), name='minhas_solicitacoes'),

    # Avaliações
    path('avaliacoes/<int:avaliado_id>/', AvaliarUsuarioView.as_view(), name='avaliar_usuario'),

    # Usuários (extra, opcional)
    path('usuarios/', UsuarioListView.as_view(), name='listar_usuarios'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)