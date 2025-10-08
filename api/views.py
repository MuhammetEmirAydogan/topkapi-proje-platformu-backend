# api/views.py

from rest_framework import generics, permissions
from .permissions import IsOwnerOrReadOnly
from .models import User, Profile, ExpertiseArea, Project, Request
from .serializers import (
    UserSerializer,
    ProfileSerializer,
    ExpertiseAreaSerializer,
    ProjectSerializer,
    RequestSerializer,
    UserRegistrationSerializer # Yeni serializer'ımızı dahil ettik
)


# --- KULLANICI KAYIT VIEW'İ (YENİ) ---

class UserRegistrationView(generics.CreateAPIView):
    """
    Yeni kullanıcı kaydı oluşturmak için. Herkese açık.
    POST: /api/register/
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny] # Herkesin erişimine izin ver


# --- Listeleme ve Oluşturma View'leri ---

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by('first_name')
    serializer_class = UserSerializer


class ProfileListView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class RequestListView(generics.ListCreateAPIView):
    queryset = Request.objects.all().order_by('-request_date')
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class ExpertiseAreaListView(generics.ListCreateAPIView):
    queryset = ExpertiseArea.objects.all().order_by('name')
    serializer_class = ExpertiseAreaSerializer


# --- Detay, Güncelleme ve Silme View'leri ---

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class RequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


class ExpertiseAreaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExpertiseArea.objects.all()
    serializer_class = ExpertiseAreaSerializer