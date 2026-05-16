from django.contrib import admin
from apps.servicos.models import DimTipoServico, DimServico


@admin.register(DimTipoServico)
class DimTipoServicoAdmin(admin.ModelAdmin):
    list_display = ['cod_tipo_servico', 'descricao_tipo_servico']


@admin.register(DimServico)
class DimServicoAdmin(admin.ModelAdmin):
    list_display = ['cod_servico', 'descricao_servico', 'cod_tipo_servico', 'valor_sugerido', 'desativado']
    list_filter = ['cod_tipo_servico', 'desativado']
