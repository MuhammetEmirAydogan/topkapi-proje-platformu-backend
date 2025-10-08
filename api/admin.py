# api/admin.py

from django.contrib import admin
# Modellerimizi bu dosyaya dahil ediyoruz
from .models import User, Profile, ExpertiseArea, Project, Request

# Her modelin admin panelinde görünmesi için onu "kaydetmemiz" (register) gerekir.

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(ExpertiseArea)
admin.site.register(Project)
admin.site.register(Request)