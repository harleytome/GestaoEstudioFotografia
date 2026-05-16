from django.urls import path
from apps.servicos import views

urlpatterns = [
    path('', views.TipoServicoListView.as_view(), name='tipo_servico_list'),
    path('novo/', views.TipoServicoCreateView.as_view(), name='tipo_servico_create'),
    path('<int:pk>/editar/', views.TipoServicoUpdateView.as_view(), name='tipo_servico_edit'),
]
