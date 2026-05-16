import os
from django.conf import settings
from docxtpl import DocxTemplate
from apps.ordens.models import FatoServico
from apps.contratos.models import DimContrato


def gerar_contrato(ordem, template_path, status_contrato='ATIVO'):
    cliente = ordem.cod_cliente
    servico = ordem.cod_servico
    tipo_servico = servico.cod_tipo_servico

    context = {
        'nome_completo': cliente.nome_completo or '',
        'endereco': cliente.endereco or '',
        'numero': cliente.numero or '',
        'complemento': cliente.complemento or '',
        'cidade': cliente.cidade or '',
        'estado': cliente.estado or '',
        'cep': cliente.cep or '',
        'bairro': cliente.bairro or '',
        'cpf': cliente.cpf or '',
        'rg': cliente.rg or '',
        'descrição_servico': ordem.descricao_servico,
        'data_servico': ordem.data_servico.strftime('%d/%m/%Y') if ordem.data_servico else '',
        'valor_sugerido': f'R$ {ordem.valor_sugerido:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.') if ordem.valor_sugerido else '',
        'formas_pagamento': ordem.formas_pagamento,
        'observacao': ordem.observacao or '',
        'nr_ordem_servico': str(ordem.nr_ordem_servico),
    }

    doc = DocxTemplate(template_path)
    doc.render(context)

    data_str = ordem.data_servico.strftime('%Y%m%d') if ordem.data_servico else 'sem_data'
    tipo_nome = tipo_servico.descricao_tipo_servico.replace(' ', '_') if tipo_servico.descricao_tipo_servico else 'servico'
    filename = f'{ordem.nr_ordem_servico}_{tipo_nome}_{data_str}.docx'

    contratos_dir = os.path.join(settings.MEDIA_ROOT, 'contratos')
    os.makedirs(contratos_dir, exist_ok=True)
    filepath = os.path.join(contratos_dir, filename)
    doc.save(filepath)

    contrato = DimContrato.objects.create(
        nr_ordem_servico=ordem,
        cod_cliente=cliente,
        nome_cliente=cliente.nome_completo or '',
        nome_arquivo=filename,
        status_contrato=status_contrato,
    )

    return contrato, filename
