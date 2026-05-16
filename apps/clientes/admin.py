from django.contrib import admin
from apps.clientes.models import DimCliente


@admin.register(DimCliente)
class DimClienteAdmin(admin.ModelAdmin):
    list_display = ['cod_cliente', 'nome_completo', 'cpf', 'cnpj', 'tipo_pessoa', 'suspenso']
    search_fields = ['nome_completo', 'cpf', 'cnpj']
