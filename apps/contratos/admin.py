from django.contrib import admin
from apps.contratos.models import DimContrato


@admin.register(DimContrato)
class DimContratoAdmin(admin.ModelAdmin):
    list_display = ['nr_contrato', 'nr_ordem_servico', 'nome_cliente', 'data_criacao', 'status_contrato']
    list_filter = ['status_contrato']
