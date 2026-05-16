from django import forms
from apps.contratos.models import DimContrato
from apps.ordens.models import FatoServico


class ContratoForm(forms.ModelForm):
    class Meta:
        model = DimContrato
        fields = ['nr_ordem_servico', 'status_contrato']


class ContratoStatusForm(forms.ModelForm):
    class Meta:
        model = DimContrato
        fields = ['status_contrato']


class RelatorioContratoForm(forms.Form):
    data_inicio = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'type': 'date'})
    )
    data_fim = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'type': 'date'})
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos')] + DimContrato.STATUS_CHOICES
    )
