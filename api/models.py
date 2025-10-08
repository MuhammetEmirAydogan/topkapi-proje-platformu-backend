# api/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings # Proje ayarlarından AUTH_USER_MODEL'i çekmek için


# --- Özel Kullanıcı Modelimiz ve Yöneticisi ---

class UserManager(BaseUserManager):
    """
    Django'ya özel kullanıcı modelimizi nasıl yöneteceğini öğreten sınıf.
    Email'i, username yerine kullanacağız.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email adresi zorunludur.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Projemizin temel kullanıcı modeli.
    """
    ROLE_CHOICES = (
        ('student', 'Öğrenci'),
        ('academic', 'Akademisyen'),
        ('admin', 'Admin'),
    )
    
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True) # Admin onayına kadar False olabilir
    is_staff = models.BooleanField(default=False) # Admin paneline erişim için
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


# --- Diğer Modellerimiz ---

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, verbose_name="Profil Fotoğrafı")
    department = models.CharField(max_length=100, verbose_name="Bölüm")
    
    # Öğrenciye özel alanlar
    student_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Öğrenci Numarası")

    # Akademisyene özel alanlar
    title = models.CharField(max_length=50, null=True, blank=True, verbose_name="Unvan")
    bio = models.TextField(null=True, blank=True, verbose_name="Hakkında")
    student_quota = models.PositiveIntegerField(default=0, verbose_name="Öğrenci Kontenjanı")
    expertise_areas = models.ManyToManyField('ExpertiseArea', blank=True, verbose_name="Uzmanlık Alanları")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} Profili"

class ExpertiseArea(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    STATUS_CHOICES = (
        ('advisor_needed', 'Danışman Aranıyor'),
        ('request_sent', 'Talep Gönderildi'),
        ('approved', 'Onaylandı'),
        ('rejected', 'Reddedildi'),
    )

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255, verbose_name="Proje Başlığı")
    description = models.TextField(verbose_name="Proje Açıklaması")
    keywords = models.CharField(max_length=255, verbose_name="Anahtar Kelimeler")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='advisor_needed')
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_academic = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_projects')

    def __str__(self):
        return self.title

class Request(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Beklemede'),
        ('academic_approved', 'Akademisyen Onayladı'),
        ('admin_approved', 'Admin Onayladı'),
        ('rejected', 'Reddedildi'),
    )
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='requests')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_requests')
    academic = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.first_name}'den {self.academic.first_name}'e talep"