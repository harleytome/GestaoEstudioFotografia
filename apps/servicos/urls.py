from django.urls import path
from apps.servicos import views
from apps.servicos.views_api import servico_api_detail

urlpatterns = [
    path('', views.ServicoListView.as_view(), name='servico_list'),
    path('novo/', views.ServicoCreateView.as_view(), name='servico_create'),
    path('api/<int:pk>/', servico_api_detail, name='servico_api_detail'),
    path('<int:pk>/editar/', views.ServicoUpdateView.as_view(), name='servico_edit'),
    path('<int:pk>/desativar/', views.ServicoToggleView.as_view(), name='servico_desativar'),
]
