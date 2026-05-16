from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from apps.ordens.models import FatoServico
from apps.ordens.forms import OrdemForm, OrdemStatusForm


class OrdemListView(LoginRequiredMixin, ListView):
    model = FatoServico
    template_name = 'ordens/list.html'
    context_object_name = 'ordens'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('cod_cliente', 'cod_servico')
        status = self.request.GET.get('status')
        q = self.request.GET.get('q')
        if status:
            qs = qs.filter(status_ordem_servico=status)
        if q:
            qs = qs.filter(
                models.Q(cod_cliente__nome_completo__icontains=q) |
                models.Q(nr_ordem_servico__icontains=q)
            )
        return qs.order_by('-nr_ordem_servico')


class OrdemCreateView(LoginRequiredMixin, CreateView):
    model = FatoServico
    form_class = OrdemForm
    template_name = 'ordens/form.html'
    success_url = reverse_lazy('ordem_list')

    def get_initial(self):
        initial = super().get_initial()
        servico_id = self.request.GET.get('servico')
        if servico_id:
            from apps.servicos.models import DimServico
            try:
                servico = DimServico.objects.get(pk=servico_id)
                initial['cod_servico'] = servico
                initial['descricao_servico'] = servico.descricao_servico
                if servico.valor_sugerido:
                    v = float(servico.valor_sugerido)
                    valor_br = f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
                    initial['valor_sugerido'] = f'R$ {valor_br}'
            except DimServico.DoesNotExist:
                pass
        return initial


class OrdemUpdateView(LoginRequiredMixin, UpdateView):
    model = FatoServico
    form_class = OrdemForm
    template_name = 'ordens/form.html'
    success_url = reverse_lazy('ordem_list')


class OrdemDetailView(LoginRequiredMixin, DetailView):
    model = FatoServico
    template_name = 'ordens/detail.html'
    context_object_name = 'ordem'


class OrdemStatusView(LoginRequiredMixin, UpdateView):
    model = FatoServico
    form_class = OrdemStatusForm
    template_name = 'ordens/change_status.html'
    success_url = reverse_lazy('ordem_list')
