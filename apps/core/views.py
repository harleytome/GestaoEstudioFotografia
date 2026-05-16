from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


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
