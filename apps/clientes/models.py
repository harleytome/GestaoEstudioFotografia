from django.db import models


class DimCliente(models.Model):
    cod_cliente = models.AutoField(primary_key=True)
    data_cadastro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    nome_completo = models.CharField(max_length=100, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    endereco = models.CharField(max_length=50, null=True, blank=True)
    numero = models.CharField(max_length=5, null=True, blank=True)
    bairro = models.CharField(max_length=30, null=True, blank=True)
    complemento = models.CharField(max_length=30, null=True, blank=True)
    cidade = models.CharField(max_length=30, null=True, blank=True)
    cep = models.CharField(max_length=10, null=True, blank=True)
    estado = models.CharField(max_length=2, null=True, blank=True)
    email_contato = models.EmailField(max_length=45, null=True, blank=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    celular = models.CharField(max_length=15, null=True, blank=True)
    cpf = models.CharField(max_length=15, null=True, blank=True)
    rg = models.CharField(max_length=15, null=True, blank=True)
    tipo_pessoa = models.CharField(max_length=1, default='F')
    cnpj = models.CharField(max_length=20, null=True, blank=True)
    inscricao = models.CharField(max_length=20, null=True, blank=True)
    nosconheceu = models.CharField(max_length=45, null=True, blank=True)
    mailing = models.CharField(max_length=3, default='SIM')
    observacao = models.CharField(max_length=200, null=True, blank=True)
    suspenso = models.BooleanField(default=False)

    class Meta:
        db_table = 'DIM_CLIENTES'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f'{self.cod_cliente} - {self.nome_completo or "Sem nome"}'
