# core/urls.py

from django.contrib import admin
from django.urls import path, include
# Dokümantasyon için gerekli view'leri dahil ediyoruz
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Bizim API URL'lerimiz
    path('api/', include('api.urls')),

    # --- YENİ DOKÜMANTASYON URL'LERİ ---
    # API şemasını oluşturan adres
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Dokümantasyonun Swagger arayüzü ile sunulduğu adres
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Dokümantasyonun Redoc arayüzü ile sunulduğu adres
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]