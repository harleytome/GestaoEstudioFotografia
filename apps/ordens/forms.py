import re
from decimal import Decimal, InvalidOperation

from django import forms
from apps.ordens.models import FatoServico


class OrdemForm(forms.ModelForm):
    valor_sugerido = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control currency-mask',
            'placeholder': 'R$ 0,00',
            'style': 'text-align: right;',
        }),
    )

    class Meta:
        model = FatoServico
        exclude = ['nr_ordem_servico']
        widgets = {
            'data_servico': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
            'descricao_servico': forms.Textarea(attrs={
                'cols': 40, 'rows': 5,
                'class': 'form-control',
                'maxlength': 200,
            }),
            'formas_pagamento': forms.Textarea(attrs={
                'cols': 40, 'rows': 5,
                'class': 'form-control',
                'maxlength': 200,
            }),
            'observacao': forms.Textarea(attrs={
                'cols': 40, 'rows': 3,
                'class': 'form-control',
                'maxlength': 200,
            }),
        }

    def clean_valor_sugerido(self):
        valor_raw = self.data.get('valor_sugerido', '').strip()
        if not valor_raw:
            return None
        valor_clean = re.sub(r'[R$\s\u00a0]', '', valor_raw)
        valor_clean = valor_clean.replace('.', '').replace(',', '.')
        try:
            return Decimal(valor_clean)
        except InvalidOperation:
            raise forms.ValidationError('Informe um valor válido.')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_servico'].required = True
        self.fields['cod_servico'].label_from_instance = lambda obj: f'{obj.cod_servico} - {obj.nome_servico}'
        if self.instance and self.instance.pk and self.instance.valor_sugerido is not None:
            valor = self.instance.valor_sugerido
            valor_br = f'{valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
            self.initial['valor_sugerido'] = f'R$ {valor_br}'


class OrdemStatusForm(forms.ModelForm):
    class Meta:
        model = FatoServico
        fields = ['status_ordem_servico']
