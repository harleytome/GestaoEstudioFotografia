from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('clientes/', include('apps.clientes.urls')),
    path('tipos-servico/', include('apps.servicos.tipo_urls')),
    path('servicos/', include('apps.servicos.urls')),
    path('ordens/', include('apps.ordens.urls')),
    path('contratos/', include('apps.contratos.urls')),
    path('config/', include('apps.core.urls')),
    path('', RedirectView.as_view(url='/ordens/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
