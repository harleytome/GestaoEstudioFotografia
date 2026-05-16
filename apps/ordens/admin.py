from django.contrib import admin
from apps.ordens.models import FatoServico


@admin.register(FatoServico)
class FatoServicoAdmin(admin.ModelAdmin):
    list_display = ['nr_ordem_servico', 'cod_cliente', 'cod_servico', 'data_servico', 'status_ordem_servico']
    list_filter = ['status_ordem_servico']
