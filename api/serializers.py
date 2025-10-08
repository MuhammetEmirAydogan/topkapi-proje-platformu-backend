# api/serializers.py

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Profile, ExpertiseArea, Project, Request

# --- KAYIT VE KULLANICI İŞLEMLERİ İÇİN SERIALIZER'LAR (YENİ) ---

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Yeni kullanıcı kaydı için serializer.
    Şifre doğrulama ve hash'leme işlemlerini yapar.
    """
    # write_only=True: Bu alanın sadece veri yazarken (kayıt olurken)
    # kullanılabileceğini, API'den veri okunurken asla gösterilmeyeceğini belirtir.
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label="Şifre Tekrarı")

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password2', 'role')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'role': {'required': True} # Rolün kayıt sırasında zorunlu olmasını sağlıyoruz
        }

    def validate(self, attrs):
        """
        İki şifrenin birbiriyle eşleşip eşleşmediğini kontrol eder.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Şifreler uyuşmuyor."})
        return attrs

    def create(self, validated_data):
        """
        Doğrulanmış veriden yeni bir kullanıcı oluşturur.
        """
        # Şifreleri validated_data'dan ayırıyoruz, çünkü create_user metodu şifreyi ayrı alır.
        validated_data.pop('password2')
        password = validated_data.pop('password')

        # UserManager'daki create_user metodunu kullanıyoruz
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        return user


# --- İç İçe Kullanım İçin Yardımcı Serializer'lar ---

class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class ProjectSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title']


# --- Ana Modeller İçin Serializer'lar ---

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['role']


class ExpertiseAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertiseArea
        fields = ['id', 'name']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSummarySerializer(read_only=True)
    expertise_areas = ExpertiseAreaSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user', 'department', 'student_number', 'title', 'bio',
            'student_quota', 'expertise_areas', 'profile_picture'
        ]


class ProjectSerializer(serializers.ModelSerializer):
    student = UserSummarySerializer(read_only=True)
    assigned_academic = UserSummarySerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'keywords', 'status', 'status_display',
            'created_at', 'student', 'assigned_academic'
        ]


class RequestSerializer(serializers.ModelSerializer):
    project = ProjectSummarySerializer(read_only=True)
    student = UserSummarySerializer(read_only=True)
    academic = UserSummarySerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Request
        fields = [
            'id', 'project', 'student', 'academic', 'status',
            'status_display', 'request_date'
        ]