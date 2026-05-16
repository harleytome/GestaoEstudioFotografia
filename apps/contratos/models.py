from django.db import models
from apps.ordens.models import FatoServico
from apps.clientes.models import DimCliente


class DimContrato(models.Model):
    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('CANCELADO', 'Cancelado'),
        ('FINALIZADO', 'Finalizado'),
    ]

    nr_contrato = models.AutoField(primary_key=True)
    nr_ordem_servico = models.ForeignKey(
        FatoServico, on_delete=models.PROTECT,
        db_column='nr_ordem_servico',
        verbose_name='Ordem de Serviço'
    )
    cod_cliente = models.ForeignKey(
        DimCliente, on_delete=models.PROTECT,
        db_column='cod_cliente',
        verbose_name='Cliente'
    )
    nome_cliente = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)
    nome_arquivo = models.CharField(max_length=255)
    status_contrato = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='ATIVO'
    )

    class Meta:
        db_table = 'DIM_CONTRATOS'
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'

    def __str__(self):
        return f'Contrato #{self.nr_contrato} - OS #{self.nr_ordem_servico.nr_ordem_servico}'
