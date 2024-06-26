from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.main, name="main"),
    path('profile/', views.profile_view, name="profile"),
    path('register/', views.register_view, name="register"),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('add_request/', views.add_request, name='add_request'),
    path('mobile_internet/', views.mobile_internet, name='mobile_internet'),
    path('wifi/', views.wifi, name='wifi'),
    path('wifi_tv/', views.wifi_tv, name='wifi_tv'),
    path('remove_service/<int:service_id>/', views.remove_service, name='remove_service'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

