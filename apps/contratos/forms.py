from django import forms
from apps.contratos.models import DimContrato
from apps.ordens.models import FatoServico


class ContratoForm(forms.ModelForm):
    class Meta:
        model = DimContrato
        fields = ['nr_ordem_servico', 'status_contrato']


class ContratoStatusForm(forms.ModelForm):
    nf = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'max-width:300px',
            'placeholder': 'Número da Nota Fiscal',
        }),
        label='Nota Fiscal',
    )

    class Meta:
        model = DimContrato
        fields = ['status_contrato']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('status_contrato') == 'FINALIZADO' and not cleaned_data.get('nf'):
            self.add_error('nf', 'Informe o número da nota fiscal para finalizar.')
        return cleaned_data


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
