from django.db import models


class DimTipoServico(models.Model):
    cod_tipo_servico = models.IntegerField(primary_key=True)
    descricao_tipo_servico = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'DIM_TIPO_SERVICOS'
        verbose_name = 'Tipo de Serviço'
        verbose_name_plural = 'Tipos de Serviço'

    def __str__(self):
        return f'{self.cod_tipo_servico} - {self.descricao_tipo_servico}'


class DimServico(models.Model):
    cod_servico = models.AutoField(primary_key=True)
    cod_tipo_servico = models.ForeignKey(
        DimTipoServico, on_delete=models.PROTECT,
        db_column='cod_tipo_servico',
        verbose_name='Tipo de Serviço'
    )
    nome_servico = models.CharField(max_length=100, verbose_name='Nome do Serviço', default='')
    descricao_servico = models.CharField(max_length=200)
    valor_sugerido = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    desativado = models.BooleanField(default=False)

    class Meta:
        db_table = 'DIM_SERVICOS'
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

    def __str__(self):
        return f'{self.cod_servico} - {self.descricao_servico}'
