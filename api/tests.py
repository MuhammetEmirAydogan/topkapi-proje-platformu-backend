# api/tests.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User, Project

class UserRegistrationTest(APITestCase):
    """
    Kullanıcı Kayıt API'si (/api/register/) için test senaryoları.
    """
    def test_student_registration_successful(self):
        data = {
            "email": "testogrenci@topkapi.edu.tr",
            "first_name": "Test",
            "last_name": "Ogrenci",
            "password": "GucluSifre123!",
            "password2": "GucluSifre123!",
            "role": "student"
        }
        url = reverse('api:register')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=data['email']).exists())
        user = User.objects.get(email=data['email'])
        self.assertEqual(user.role, 'student')
        print("\n[SUCCESS] Öğrenci Kayıt Testi Başarılı!")


# --- GÜVENLİK TESTİ SINIFI ---
class ProjectPermissionsTest(APITestCase):
    """
    Proje güncelleme ve silme yetkilerini test eder.
    """

    def setUp(self):
        """Her test metodundan önce çalışacak hazırlık fonksiyonu."""
        self.user_owner = User.objects.create_user(
            email='owner@test.com',
            password='password123',
            first_name='Proje',
            last_name='Sahibi',
            role='student'
        )
        self.user_imposter = User.objects.create_user(
            email='imposter@test.com',
            password='password123',
            first_name='Yetkisiz',
            last_name='Kullanici',
            role='student'
        )
        self.project = Project.objects.create(
            student=self.user_owner,
            title="Sahibinin Projesi",
            description="Bu proje user_owner'a aittir.",
            keywords="test, proje" # Zorunlu alanı ekledik
        )
        self.url = reverse('api:project-detail', kwargs={'pk': self.project.pk})

    def test_imposter_cannot_update_project(self):
        """Yetkisiz kullanıcının projeyi GÜNCELLEYEMEDİĞİNİ test eder."""
        self.client.force_authenticate(user=self.user_imposter)
        updated_data = {'title': 'Bu başlık değişmemeli'}
        response = self.client.patch(self.url, updated_data, format='json') # put -> patch
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("\n[SUCCESS] Yetkisiz Kullanıcı Güncelleme Testi Başarılı!")

    def test_owner_can_update_project(self):
        """Proje sahibinin projeyi GÜNCELLEYEBİLDİĞİNİ test eder."""
        self.client.force_authenticate(user=self.user_owner)
        updated_data = {'title': 'Bu başlık değişmeli', 'description': 'Açıklama da değişti'}
        
        # --- DEĞİŞİKLİK BURADA ---
        response = self.client.patch(self.url, updated_data, format='json') # put -> patch olarak değiştirildi

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, 'Bu başlık değişmeli')
        print("\n[SUCCESS] Proje Sahibi Güncelleme Testi Başarılı!")

    def test_imposter_cannot_delete_project(self):
        """Yetkisiz kullanıcının projeyi SİLEMEDİĞİNİ test eder."""
        self.client.force_authenticate(user=self.user_imposter)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("\n[SUCCESS] Yetkisiz Kullanıcı Silme Testi Başarılı!")

    def test_owner_can_delete_project(self):
        """Proje sahibinin projeyi SİLEBİLDİĞİNİ test eder."""
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print("\n[SUCCESS] Proje Sahibi Silme Testi Başarılı!")