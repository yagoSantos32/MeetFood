from django.db import models
from django.utils import timezone

class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.nome} - {self.uf}"



class Usuario(models.Model):  # RF01
    TIPO_USUARIO_CHOICES = [
        ('restaurante', 'Restaurante'),
        ('instituicao', 'Instituição'),
    ]

    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)  
    telefone = models.CharField(max_length=15)
    tipo_usuario = models.CharField(max_length=14, choices=TIPO_USUARIO_CHOICES)
    cpf_cnpj = models.CharField(max_length=18, unique=True)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome




# -------------------------------
# DOAÇÃO
# -------------------------------
class Doacao(models.Model):
    restaurante = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    status = models.CharField(max_length=20)
    disponivel = models.BooleanField(default=True)
    imagem = models.ImageField(upload_to='imagens/', null=True, blank=True)
    data = models.DateTimeField(default=timezone.now)  # ✔️ novo campo

    def __str__(self):
        return self.titulo



# -------------------------------
# SOLICITAÇÃO
# -------------------------------
class Solicitacao(models.Model):
    instituicao = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='solicitacoes',
                                     limit_choices_to={'tipo_usuario': 'instituicao'})
    doacao = models.ForeignKey(Doacao, on_delete=models.CASCADE)
    mensagem = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado')
    ], default='pendente')

    def __str__(self):
        return f"Solicitação de {self.instituicao.nome} - {self.doacao.titulo}"


# -------------------------------
# MENSAGEM ENTRE USUÁRIOS
# -------------------------------
class Mensagem(models.Model):
    remetente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensagens_recebidas')
    texto = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"De {self.remetente.nome} para {self.destinatario.nome}"


# -------------------------------
# AVALIAÇÃO
# -------------------------------
class Avaliacao(models.Model):
    avaliador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='avaliacoes_feitas')
    avaliado = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='avaliacoes_recebidas')
    nota = models.IntegerField()
    comentario = models.TextField(blank=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.avaliador.nome} para {self.avaliado.nome} ({self.nota})"
