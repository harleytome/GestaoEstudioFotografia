from django.urls import path
from apps.core import views

urlpatterns = [
    path('cores/', views.ThemeConfigView.as_view(), name='theme_config'),
    path('relatorios/compromissos/', views.relatorio_compromissos, name='relatorio_compromissos'),
    path('relatorios/financeiro/', views.relatorio_financeiro, name='relatorio_financeiro'),
]
