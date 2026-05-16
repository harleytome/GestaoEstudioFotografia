import os
import mammoth
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.http import FileResponse, Http404, HttpResponseBadRequest
from django.db import models
from django.contrib import messages
from apps.contratos.models import DimContrato
from apps.contratos.forms import ContratoForm, ContratoStatusForm, RelatorioContratoForm
from apps.ordens.models import FatoServico
from apps.contratos.utils import gerar_contrato
from django.conf import settings


class ContratoListView(LoginRequiredMixin, ListView):
    model = DimContrato
    template_name = 'contratos/list.html'
    context_object_name = 'contratos'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('nr_ordem_servico', 'cod_cliente')
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')
        status = self.request.GET.get('status')

        if data_inicio:
            qs = qs.filter(data_criacao__date__gte=data_inicio)
        if data_fim:
            qs = qs.filter(data_criacao__date__lte=data_fim)
        if status:
            qs = qs.filter(status_contrato=status)

        return qs.order_by('-data_criacao')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = RelatorioContratoForm(self.request.GET or None)
        ctx['STATUS_CHOICES'] = DimContrato.STATUS_CHOICES
        return ctx


class ContratoCreateView(LoginRequiredMixin, CreateView):
    model = DimContrato
    form_class = ContratoForm
    template_name = 'contratos/form.html'
    success_url = reverse_lazy('contrato_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['ordens'] = FatoServico.objects.filter(status_ordem_servico='EM_ABERTO')
        ctx['templates_disponiveis'] = self._listar_templates()
        return ctx

    def _listar_templates(self):
        templates_dir = os.path.join(settings.BASE_DIR, 'templates_contratos')
        os.makedirs(templates_dir, exist_ok=True)
        arquivos = []
        for f in os.listdir(templates_dir):
            if f.endswith('.docx'):
                arquivos.append(f)
        return arquivos

    def form_valid(self, form):
        ordem_pk = self.request.POST.get('nr_ordem_servico')
        template_nome = self.request.POST.get('template_arquivo')

        if not ordem_pk or not template_nome:
            form.add_error(None, 'Selecione uma ordem de serviço e um template.')
            return self.form_invalid(form)

        ordem = get_object_or_404(FatoServico, pk=ordem_pk)
        template_path = os.path.join(settings.BASE_DIR, 'templates_contratos', template_nome)

        if not os.path.exists(template_path):
            form.add_error(None, f'Template "{template_nome}" não encontrado.')
            return self.form_invalid(form)

        status = form.cleaned_data.get('status_contrato', 'ATIVO')
        gerar_contrato(ordem, template_path, status)

        return redirect(self.success_url)


class ContratoDetailView(LoginRequiredMixin, DetailView):
    model = DimContrato
    template_name = 'contratos/detail.html'
    context_object_name = 'contrato'


class ContratoDocxView(LoginRequiredMixin, TemplateView):
    template_name = 'contratos/docx_view.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        contrato = get_object_or_404(DimContrato, pk=self.kwargs['pk'])
        docx_path = os.path.join(settings.MEDIA_ROOT, 'contratos', contrato.nome_arquivo)

        if not os.path.exists(docx_path):
            ctx['erro'] = 'Arquivo do contrato não encontrado no servidor.'
            return ctx

        with open(docx_path, 'rb') as f:
            result = mammoth.convert_to_html(f)
            ctx['html_content'] = result.value

        ctx['contrato'] = contrato
        return ctx


class ContratoStatusView(LoginRequiredMixin, UpdateView):
    model = DimContrato
    form_class = ContratoStatusForm
    template_name = 'contratos/change_status.html'
    success_url = reverse_lazy('contrato_list')

    def form_valid(self, form):
        contrato = self.get_object()
        if contrato.status_contrato in ('FINALIZADO', 'CANCELADO'):
            form.add_error('status_contrato',
                'Este contrato já foi finalizado ou cancelado e não pode mais ser alterado.')
            return self.form_invalid(form)

        novo_status = form.cleaned_data['status_contrato']
        ordem = contrato.nr_ordem_servico

        if novo_status == 'CANCELADO':
            ordem.status_ordem_servico = 'CANCELADO'
        elif novo_status == 'FINALIZADO':
            ordem.status_ordem_servico = 'EXECUTADO'

        ordem.save()
        return super().form_valid(form)


class ContratoDownloadView(LoginRequiredMixin, View):
    def get(self, request, pk):
        contrato = get_object_or_404(DimContrato, pk=pk)
        docx_path = os.path.join(settings.MEDIA_ROOT, 'contratos', contrato.nome_arquivo)
        if not os.path.exists(docx_path):
            raise Http404('Arquivo não encontrado.')
        response = FileResponse(
            open(docx_path, 'rb'),
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        )
        response['Content-Disposition'] = f'attachment; filename="{contrato.nome_arquivo}"'
        return response


TEMPLATES_DIR = os.path.join(settings.BASE_DIR, 'templates_contratos')


class TemplateListView(LoginRequiredMixin, View):
    template_name = 'contratos/template_list.html'

    def get_templates(self):
        os.makedirs(TEMPLATES_DIR, exist_ok=True)
        arquivos = []
        for f in sorted(os.listdir(TEMPLATES_DIR)):
            if f.endswith('.docx') and not f.startswith('._tmp_'):
                arquivos.append(f)
        return arquivos

    def get(self, request):
        return self._render(request)

    def _render(self, request, erro=None, arquivo_conflito=None, tmp_arquivo=None):
        return render(request, self.template_name, {
            'templates': self.get_templates(),
            'erro': erro,
            'arquivo_conflito': arquivo_conflito,
            'tmp_arquivo': tmp_arquivo,
        })

    def post(self, request):
        sobrescrever = request.POST.get('sobrescrever') == '1'
        tmp_arquivo = request.POST.get('tmp_arquivo', '')

        if tmp_arquivo:
            tmp_path = os.path.join(TEMPLATES_DIR, f'._tmp_{tmp_arquivo}')
            destino = os.path.join(TEMPLATES_DIR, tmp_arquivo)

            if sobrescrever and os.path.exists(tmp_path):
                os.replace(tmp_path, destino)
                messages.success(request, f'Template "{tmp_arquivo}" sobrescrito com sucesso.')
                return redirect('template_list')

            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            return self._render(request, erro='Operação cancelada.')

        arquivo = request.FILES.get('arquivo')
        if not arquivo:
            return self._render(request, erro='Selecione um arquivo para upload.')

        if not arquivo.name.endswith('.docx'):
            return self._render(request, erro='Apenas arquivos .docx são permitidos.')

        destino = os.path.join(TEMPLATES_DIR, arquivo.name)

        if os.path.exists(destino) and not sobrescrever:
            tmp_path = os.path.join(TEMPLATES_DIR, f'._tmp_{arquivo.name}')
            with open(tmp_path, 'wb+') as f:
                for chunk in arquivo.chunks():
                    f.write(chunk)
            return self._render(request, arquivo_conflito=arquivo.name, tmp_arquivo=arquivo.name)

        with open(destino, 'wb+') as f:
            for chunk in arquivo.chunks():
                f.write(chunk)

        messages.success(request, f'Template "{arquivo.name}" salvo com sucesso.')
        return redirect('template_list')


class TemplateDocxView(LoginRequiredMixin, TemplateView):
    template_name = 'contratos/template_view.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        filename = self.kwargs['filename']
        filepath = os.path.join(TEMPLATES_DIR, filename)

        if not os.path.exists(filepath):
            ctx['erro'] = 'Arquivo não encontrado.'
            return ctx

        with open(filepath, 'rb') as f:
            result = mammoth.convert_to_html(f)
            ctx['html_content'] = result.value

        ctx['filename'] = filename
        return ctx


class TemplateDownloadView(LoginRequiredMixin, View):
    def get(self, request, filename):
        filepath = os.path.join(TEMPLATES_DIR, filename)
        if not os.path.exists(filepath):
            raise Http404('Arquivo não encontrado.')
        response = FileResponse(
            open(filepath, 'rb'),
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


class TemplateDeleteView(LoginRequiredMixin, View):
    def post(self, request, filename):
        filepath = os.path.join(TEMPLATES_DIR, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            messages.success(request, f'Template "{filename}" removido.')
        return redirect('template_list')
