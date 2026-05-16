from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.servicos.models import DimTipoServico, DimServico
from apps.servicos.forms import TipoServicoForm, ServicoForm


class TipoServicoListView(LoginRequiredMixin, ListView):
    model = DimTipoServico
    template_name = 'servicos/tipo_list.html'
    context_object_name = 'tipos'


class TipoServicoCreateView(LoginRequiredMixin, CreateView):
    model = DimTipoServico
    form_class = TipoServicoForm
    template_name = 'servicos/tipo_form.html'
    success_url = reverse_lazy('tipo_servico_list')


class TipoServicoUpdateView(LoginRequiredMixin, UpdateView):
    model = DimTipoServico
    form_class = TipoServicoForm
    template_name = 'servicos/tipo_form.html'
    success_url = reverse_lazy('tipo_servico_list')


class ServicoListView(LoginRequiredMixin, ListView):
    model = DimServico
    template_name = 'servicos/list.html'
    context_object_name = 'servicos'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        tipo = self.request.GET.get('tipo')
        if q:
            qs = qs.filter(
                Q(descricao_servico__icontains=q) | Q(nome_servico__icontains=q)
            )
        if tipo:
            qs = qs.filter(cod_tipo_servico_id=tipo)
        return qs.select_related('cod_tipo_servico')


class ServicoCreateView(LoginRequiredMixin, CreateView):
    model = DimServico
    form_class = ServicoForm
    template_name = 'servicos/form.html'
    success_url = reverse_lazy('servico_list')


class ServicoUpdateView(LoginRequiredMixin, UpdateView):
    model = DimServico
    form_class = ServicoForm
    template_name = 'servicos/form.html'
    success_url = reverse_lazy('servico_list')


class ServicoToggleView(LoginRequiredMixin, View):
    def get(self, request, pk):
        servico = DimServico.objects.get(pk=pk)
        servico.desativado = not servico.desativado
        servico.save()
        return redirect('servico_list')
