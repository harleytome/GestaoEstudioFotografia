import calendar
import json
from datetime import date, timedelta

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.db.models import Sum

from apps.ordens.models import FatoServico
from apps.contratos.models import DimContrato
from apps.core.forms import RelatorioCompromissosForm, RelatorioFinanceiroForm


MESES = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro',
]


@login_required
def relatorio_compromissos(request):
    today = date.today()
    data_inicial = today
    data_final = today + timedelta(days=90)

    form = RelatorioCompromissosForm(request.GET or None, initial={
        'data_inicial': data_inicial,
        'data_final': data_final,
    })
    if form.is_valid():
        if form.cleaned_data['data_inicial']:
            data_inicial = form.cleaned_data['data_inicial']
        if form.cleaned_data['data_final']:
            data_final = form.cleaned_data['data_final']

    servicos = FatoServico.objects.filter(
        data_servico__date__gte=data_inicial,
        data_servico__date__lte=data_final,
        data_servico__isnull=False,
    ).select_related('cod_cliente').order_by('data_servico')

    agenda = {}
    day_services = {}
    for s in servicos:
        d = s.data_servico.date()
        d_key = d.isoformat()
        if d not in agenda:
            agenda[d] = {'EM_ABERTO': [], 'EXECUTADO': [], 'CANCELADO': []}
        agenda[d][s.status_ordem_servico].append(s)
        if d_key not in day_services:
            day_services[d_key] = []
        day_services[d_key].append({
            'nr': s.nr_ordem_servico,
            'cliente': s.cod_cliente.nome_completo or str(s.cod_cliente.cod_cliente),
            'status': s.status_ordem_servico,
            'status_display': s.get_status_ordem_servico_display(),
        })

    months_data = []
    current = data_inicial.replace(day=1)
    last = date(data_final.year, data_final.month, 1)
    while current <= last:
        weeks = calendar.monthcalendar(current.year, current.month)
        month_weeks = []
        for week in weeks:
            week_days = []
            for day_num in week:
                if day_num == 0:
                    week_days.append({'day': 0, 'servicos': None})
                else:
                    d = date(current.year, current.month, day_num)
                    week_days.append({
                        'day': day_num,
                        'date': d,
                        'servicos': agenda.get(d),
                    })
            month_weeks.append(week_days)
        months_data.append({
            'name': MESES[current.month - 1],
            'year': current.year,
            'month_num': current.month,
            'weeks': month_weeks,
        })
        if current.month == 12:
            current = date(current.year + 1, 1, 1)
        else:
            current = date(current.year, current.month + 1, 1)

    context = {
        'form': form,
        'months_data': months_data,
        'data_inicial': data_inicial,
        'data_final': data_final,
        'day_services_json': json.dumps(day_services),
    }
    return render(request, 'core/relatorio_compromissos.html', context)


@login_required
def relatorio_financeiro(request):
    today = date.today()
    data_inicio = today
    data_fim = today + timedelta(days=90)
    ordenar_por = 'data_servico'
    status_filter = None

    form = RelatorioFinanceiroForm(request.GET or None, initial={
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'ordenar_por': ordenar_por,
    })
    if form.is_valid():
        if form.cleaned_data['data_inicio']:
            data_inicio = form.cleaned_data['data_inicio']
        if form.cleaned_data['data_fim']:
            data_fim = form.cleaned_data['data_fim']
        if form.cleaned_data['ordenar_por']:
            ordenar_por = form.cleaned_data['ordenar_por']
        status_filter = form.cleaned_data.get('status_ordem')

    contratos = DimContrato.objects.select_related('nr_ordem_servico').filter(
        nr_ordem_servico__data_servico__date__gte=data_inicio,
        nr_ordem_servico__data_servico__date__lte=data_fim,
        nr_ordem_servico__data_servico__isnull=False,
    )

    if status_filter:
        contratos = contratos.filter(nr_ordem_servico__status_ordem_servico=status_filter)

    order_map = {
        'data_servico': 'nr_ordem_servico__data_servico',
        'data_criacao': 'data_criacao',
    }
    contratos = contratos.order_by(order_map.get(ordenar_por, 'nr_ordem_servico__data_servico'))

    total = contratos.aggregate(total=Sum('nr_ordem_servico__valor_sugerido'))['total'] or 0

    context = {
        'form': form,
        'contratos': contratos,
        'total': total,
        'ordenar_por': ordenar_por,
    }
    return render(request, 'core/relatorio_financeiro.html', context)


class ThemeConfigView(LoginRequiredMixin, TemplateView):
    template_name = 'core/theme_settings.html'

    def post(self, request):
        colors = {
            'bg_primary': request.POST.get('bg_primary', '#1a1a2e'),
            'bg_secondary': request.POST.get('bg_secondary', '#16213e'),
            'text_primary': request.POST.get('text_primary', '#e0e0e0'),
            'text_secondary': request.POST.get('text_secondary', '#a0a0a0'),
            'accent_color': request.POST.get('accent_color', '#0f3460'),
            'accent_hover': request.POST.get('accent_hover', '#1a4a8a'),
            'sidebar_bg': request.POST.get('sidebar_bg', '#0f3460'),
            'card_bg': request.POST.get('card_bg', '#1e2a4a'),
            'border_color': request.POST.get('border_color', '#2a3a5c'),
            'success_color': request.POST.get('success_color', '#28a745'),
            'danger_color': request.POST.get('danger_color', '#dc3545'),
            'warning_color': request.POST.get('warning_color', '#ffc107'),
        }
        request.session['theme_colors'] = colors
        return redirect('theme_config')
