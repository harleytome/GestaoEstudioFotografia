from django.urls import path
from apps.ordens import views

urlpatterns = [
    path('', views.OrdemListView.as_view(), name='ordem_list'),
    path('nova/', views.OrdemCreateView.as_view(), name='ordem_create'),
    path('<int:pk>/', views.OrdemDetailView.as_view(), name='ordem_detail'),
    path('<int:pk>/editar/', views.OrdemUpdateView.as_view(), name='ordem_edit'),
    path('<int:pk>/alterar-status/', views.OrdemStatusView.as_view(), name='ordem_status'),
]
