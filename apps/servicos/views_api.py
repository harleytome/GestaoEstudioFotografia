from django.http import JsonResponse
from apps.servicos.models import DimServico


def servico_api_detail(request, pk):
    try:
        servico = DimServico.objects.get(pk=pk)
        return JsonResponse({
            'cod_servico': servico.cod_servico,
            'nome_servico': servico.nome_servico,
            'descricao_servico': servico.descricao_servico,
            'valor_sugerido': str(servico.valor_sugerido) if servico.valor_sugerido else None,
        })
    except DimServico.DoesNotExist:
        return JsonResponse({'error': 'Serviço não encontrado'}, status=404)
