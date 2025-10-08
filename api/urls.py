# api/urls.py

from django.urls import path
from . import views
# Simple JWT'nin hazır view'lerini dahil ediyoruz
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'api'

urlpatterns = [
    # KULLANICI YÖNETİMİ URL'LERİ
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    
    # --- YENİ TOKEN URL'LERİ ---
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Bu bizim login adresimiz olacak
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # --- BİTTİ ---

    # User URLs
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),

    # Profile URLs
    path('profiles/', views.ProfileListView.as_view(), name='profile-list'),
    path('profiles/<int:pk>/', views.ProfileDetailView.as_view(), name='profile-detail'),

    # Project URLs
    path('projects/', views.ProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),

    # Request URLs
    path('requests/', views.RequestListView.as_view(), name='request-list'),
    path('requests/<int:pk>/', views.RequestDetailView.as_view(), name='request-detail'),

    # ExpertiseArea URLs
    path('expertise-areas/', views.ExpertiseAreaListView.as_view(), name='expertise-area-list'),
    path('expertise-areas/<int:pk>/', views.ExpertiseAreaDetailView.as_view(), name='expertise-area-detail'),
]