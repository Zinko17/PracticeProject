from django.contrib import admin
from .models import Service, UserProfile

# Register your models here.
admin.site.register(Service)
admin.site.register(UserProfile)