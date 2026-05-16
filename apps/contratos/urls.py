from django.urls import path
from apps.contratos import views

urlpatterns = [
    path('', views.ContratoListView.as_view(), name='contrato_list'),
    path('novo/', views.ContratoCreateView.as_view(), name='contrato_create'),
    path('<int:pk>/', views.ContratoDetailView.as_view(), name='contrato_detail'),
    path('<int:pk>/docx/', views.ContratoDocxView.as_view(), name='contrato_docx'),
    path('<int:pk>/download/', views.ContratoDownloadView.as_view(), name='contrato_download'),
    path('<int:pk>/alterar-status/', views.ContratoStatusView.as_view(), name='contrato_status'),
]
