# api/permissions.py

from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Özel yetki sınıfı. Sadece objenin sahibi olanların yazma izni
    olmasını, diğerlerinin ise sadece okuma izni olmasını sağlar.
    """
    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS gibi güvenli (sadece okuma amaçlı) isteklere her zaman izin verilir.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Yazma (PUT, DELETE) izinleri ise sadece projenin sahibi olan
        # öğrenciye verilir.
        # obj -> kontrol edilen Proje nesnesi
        # obj.student -> Proje modelindeki 'student' alanı
        # request.user -> o an giriş yapmış olan kullanıcı
        return obj.student == request.user