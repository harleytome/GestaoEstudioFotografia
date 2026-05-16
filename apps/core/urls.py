from django.urls import path
from apps.core import views

urlpatterns = [
    path('cores/', views.ThemeConfigView.as_view(), name='theme_config'),
]
