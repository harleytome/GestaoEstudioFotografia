from django.http import JsonResponse
from apps.clientes.models import DimCliente


def cliente_api_search(request):
    q = request.GET.get('q', '').strip()
    if not q:
        return JsonResponse([], safe=False)
    clientes = DimCliente.objects.filter(
        nome_completo__icontains=q
    ).order_by('nome_completo')[:20]
    data = [
        {
            'cod_cliente': c.cod_cliente,
            'nome_completo': c.nome_completo or '',
        }
        for c in clientes
    ]
    return JsonResponse(data, safe=False)
