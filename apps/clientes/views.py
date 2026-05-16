from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from apps.clientes.models import DimCliente
from apps.clientes.forms import ClienteForm


class ClienteListView(LoginRequiredMixin, ListView):
    model = DimCliente
    template_name = 'clientes/list.html'
    context_object_name = 'clientes'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                models.Q(nome_completo__icontains=q) |
                models.Q(cpf__icontains=q) |
                models.Q(cnpj__icontains=q) |
                models.Q(cod_cliente__icontains=q)
            )
        return qs.order_by('nome_completo')


class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = DimCliente
    form_class = ClienteForm
    template_name = 'clientes/form.html'
    success_url = reverse_lazy('cliente_list')


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = DimCliente
    form_class = ClienteForm
    template_name = 'clientes/form.html'
    success_url = reverse_lazy('cliente_list')


class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = DimCliente
    template_name = 'clientes/detail.html'
    context_object_name = 'cliente'


class ClienteSuspendView(LoginRequiredMixin, View):
    def get(self, request, pk):
        cliente = DimCliente.objects.get(pk=pk)
        cliente.suspenso = not cliente.suspenso
        cliente.save()
        return redirect('cliente_list')
