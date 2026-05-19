from django import forms
from apps.ordens.models import FatoServico


class RelatorioCompromissosForm(forms.Form):
    data_inicial = forms.DateField(
        required=False,
        label='Data Inicial',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    data_final = forms.DateField(
        required=False,
        label='Data Final',
        widget=forms.DateInput(attrs={'type': 'date'})
    )


class RelatorioFinanceiroForm(forms.Form):
    data_inicio = forms.DateField(
        required=False,
        label='Data Início',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    data_fim = forms.DateField(
        required=False,
        label='Data Fim',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    status_ordem = forms.ChoiceField(
        required=False,
        label='Status OS',
        choices=[('', 'Todos')] + FatoServico.STATUS_CHOICES
    )
    ordenar_por = forms.ChoiceField(
        required=False,
        label='Ordenar por',
        choices=[
            ('data_servico', 'Data do Serviço'),
            ('data_criacao', 'Data de Criação'),
        ]
    )
