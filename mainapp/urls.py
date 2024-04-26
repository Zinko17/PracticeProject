from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.main, name="main")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

