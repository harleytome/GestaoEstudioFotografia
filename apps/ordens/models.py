from django.db import models
from apps.clientes.models import DimCliente
from apps.servicos.models import DimServico


class FatoServico(models.Model):
    STATUS_CHOICES = [
        ('EM_ABERTO', 'Em Aberto'),
        ('CANCELADO', 'Cancelado'),
        ('EXECUTADO', 'Executado'),
    ]

    nr_ordem_servico = models.AutoField(primary_key=True)
    cod_cliente = models.ForeignKey(
        DimCliente, on_delete=models.PROTECT,
        db_column='cod_cliente',
        verbose_name='Cliente'
    )
    cod_servico = models.ForeignKey(
        DimServico, on_delete=models.PROTECT,
        db_column='cod_servico',
        verbose_name='Serviço'
    )
    data_servico = models.DateTimeField(null=True, blank=True)
    descricao_servico = models.CharField(max_length=200)
    formas_pagamento = models.CharField(max_length=200)
    valor_sugerido = models.FloatField(null=True, blank=True)
    status_ordem_servico = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default='EM_ABERTO'
    )
    observacao = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'FATO_SERVICOS'
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'

    def __str__(self):
        return f'OS #{self.nr_ordem_servico} - {self.cod_cliente.nome_completo or self.cod_cliente.cod_cliente}'
