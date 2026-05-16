import re
from decimal import Decimal, InvalidOperation

from django import forms

from apps.servicos.models import DimTipoServico, DimServico


class TipoServicoForm(forms.ModelForm):
    class Meta:
        model = DimTipoServico
        fields = '__all__'


class ServicoForm(forms.ModelForm):
    valor_sugerido = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control currency-mask',
            'placeholder': 'R$ 0,00',
            'style': 'text-align: right;',
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.valor_sugerido is not None:
            valor = self.instance.valor_sugerido
            valor_br = f'{valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
            self.initial['valor_sugerido'] = f'R$ {valor_br}'

    class Meta:
        model = DimServico
        exclude = ['cod_servico']
        widgets = {
            'nome_servico': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 100,
            }),
            'descricao_servico': forms.Textarea(attrs={
                'cols': 40, 'rows': 5,
                'class': 'form-control',
                'maxlength': 200,
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        valor_raw = self.data.get('valor_sugerido', '').strip()
        if valor_raw:
            valor_clean = re.sub(r'[R$\s\u00a0]', '', valor_raw)
            valor_clean = valor_clean.replace('.', '').replace(',', '.')
            try:
                cleaned_data['valor_sugerido'] = Decimal(valor_clean)
            except InvalidOperation:
                self.add_error(
                    'valor_sugerido',
                    'Informe um número válido.',
                )
        return cleaned_data
