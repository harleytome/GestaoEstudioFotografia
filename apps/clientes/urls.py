from django.urls import path
from apps.clientes import views, views_api

urlpatterns = [
    path('', views.ClienteListView.as_view(), name='cliente_list'),
    path('novo/', views.ClienteCreateView.as_view(), name='cliente_create'),
    path('<int:pk>/', views.ClienteDetailView.as_view(), name='cliente_detail'),
    path('<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente_edit'),
    path('api/search/', views_api.cliente_api_search, name='cliente_api_search'),
    path('<int:pk>/suspender/', views.ClienteSuspendView.as_view(), name='cliente_suspender'),
]
