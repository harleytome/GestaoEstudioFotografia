from django import forms
from apps.clientes.models import DimCliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = DimCliente
        exclude = ['cod_cliente', 'data_cadastro']
        widgets = {
            'data_nascimento': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d',
            ),
        }
