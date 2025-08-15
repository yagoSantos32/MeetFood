from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from .models import *
from django import forms


# ---------- AUTENTICAÇÃO ----------

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            usuario = Usuario.objects.get(email=email)
            if check_password(senha, usuario.senha):
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nome'] = usuario.nome
                return redirect('index')
            else:
                messages.error(request, "Email ou senha inválidos.")
        except Usuario.DoesNotExist:
            messages.error(request, "Email ou senha inválidos.")
        
        return redirect('login')


class CadastroView(View):
    def get(self, request):
        return render(request, 'cadastro.html')

    def post(self, request):
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        telefone = request.POST.get('telefone')
        tipo_usuario = request.POST.get('tipo_usuario')
        cpf_cnpj = request.POST.get('cpf_cnpj')
        cidade_id = request.POST.get('cidade')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "Email já cadastrado.")
            return redirect('cadastro')

        senha_hash = make_password(senha)

        cidade = None
        if cidade_id:
            try:
                cidade = Cidade.objects.get(id=cidade_id)
            except Cidade.DoesNotExist:
                messages.error(request, "Cidade inválida.")
                return redirect('cadastro')

        Usuario.objects.create(
            nome=nome,
            email=email,
            senha=senha_hash,
            telefone=telefone,
            tipo_usuario=tipo_usuario,
            cpf_cnpj=cpf_cnpj,
            cidade=cidade
        )
        return redirect('login')


def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')


def index_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        request.session.flush()
        return redirect('login')

    doacoes = Doacao.objects.filter(status='disponivel')
    return render(request, 'index.html', {'usuario': usuario, 'doacoes': doacoes})
def exemplo_cards(request):
    doacoes = Doacao.objects.filter(disponivel=True)  # só as disponíveis
    return render(request, 'index.html', {'doacoes': doacoes})


# Doacao
class MinhasDoacoesView(View):
    def get(self, request):
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return redirect('login')

        usuario = Usuario.objects.get(id=usuario_id)
        doacoes = Doacao.objects.filter(restaurante=usuario)
        return render(request, 'doacoes/minhas.html', {'doacoes': doacoes})


# ---------- SOLICITAÇÕES ----------

class SolicitarDoacaoView(View):
    def get(self, request, doacao_id):
        if not request.session.get('usuario_id'):
            return redirect('login')
        doacao = get_object_or_404(Doacao, id=doacao_id)
        return render(request, 'solicitacoes/solicitar.html', {'doacao': doacao})

    def post(self, request, doacao_id):
        if not request.session.get('usuario_id'):
            return redirect('login')

        usuario = Usuario.objects.get(id=request.session['usuario_id'])
        mensagem = request.POST.get('mensagem')
        doacao = Doacao.objects.get(id=doacao_id)

        Solicitacao.objects.create(
            instituicao=usuario,
            doacao=doacao,
            mensagem=mensagem
        )
        return redirect('minhas_solicitacoes')


class MinhasSolicitacoesView(View):
    def get(self, request):
        if not request.session.get('usuario_id'):
            return redirect('login')

        usuario = Usuario.objects.get(id=request.session['usuario_id'])
        solicitacoes = Solicitacao.objects.filter(instituicao=usuario)
        return render(request, 'solicitacoes/minhas.html', {'solicitacoes': solicitacoes})



class AvaliarUsuarioView(View):
    def get(self, request, avaliado_id):
        if not request.session.get('usuario_id'):
            return redirect('login')

        avaliado = Usuario.objects.get(id=avaliado_id)
        return render(request, 'avaliacoes/avaliar.html', {'avaliado': avaliado})

    def post(self, request, avaliado_id):
        if not request.session.get('usuario_id'):
            return redirect('login')

        avaliador = Usuario.objects.get(id=request.session['usuario_id'])
        avaliado = Usuario.objects.get(id=avaliado_id)
        nota = int(request.POST.get('nota'))
        comentario = request.POST.get('comentario')

        Avaliacao.objects.create(
            avaliador=avaliador,
            avaliado=avaliado,
            nota=nota,
            comentario=comentario
        )
        return redirect('index')


# ---------- EXTRAS ----------

class UsuarioListView(View):
    def get(self, request):
        usuarios = Usuario.objects.all()
        return render(request, 'usuarios.html', {'usuarios': usuarios})


def chat_view(request):
    usuario = None
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        usuario = get_object_or_404(Usuario, id=usuario_id)
    return render(request, 'chat.html', {'usuario': usuario})

def doacoes_view(request):
    doacoes = Doacao.objects.filter(disponivel=True)
    return render(request, 'doacoes.html', {'doacoes': doacoes})

class PerfilView(View):
    def get(self, request):
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return redirect('login') 
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return redirect('login')

        return render(request, 'perfil.html', {'usuario': usuario})
    
class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'telefone', 'cidade', 'cpf_cnpj']
            # adicione outros campos que quiser permitir editar
def editar_perfil(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = EditarPerfilForm(instance=usuario)

    return render(request, 'editar_perfil.html', {'form': form})

    
class Meet(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    likes = models.ManyToManyField(Usuario, related_name='meus_meets', blank=True)
