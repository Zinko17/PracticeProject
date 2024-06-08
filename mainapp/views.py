from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, UserProfile
from .forms import UserProfileForm, UserForm, RegistrationForm

# Create your views here.

def main(request):
    services = Service.objects.all()
    return render(request, 'mainapp/main.html', {'services': services})

@login_required
def remove_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_profile.services.remove(service)
        return redirect('profile')  # Укажите URL вашего профиля
    return HttpResponseForbidden("Вы не можете удалить эту заявку.")


@login_required
def profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    service_requests = user_profile.services.all()  # Получаем все заявки пользователя
    return render(request, 'mainapp/profile.html', {'userprofile': user_profile, 'service_requests': service_requests})

from django.contrib.auth.models import User
from .forms import UserProfileForm, UserForm, RegistrationForm

def register_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # Создание пользователя с хэшированным паролем
            user = User.objects.create_user(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password'],
                email=user_form.cleaned_data['email']
            )
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'registration/registration.html', {'user_form': user_form, 'profile_form': profile_form})


def service_detail(request, service_id):
    # Получаем объект Service по его идентификатору или возвращаем 404, если он не существует
    service = get_object_or_404(Service, pk=service_id)
    return render(request, 'mainapp/service_detail.html', {'service': service})


@login_required
def add_request(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        service = Service.objects.get(pk=service_id)
        user_profile = request.user.userprofile
        user_profile.services.add(service)

        # Устанавливаем флаг в сессии, чтобы сообщить шаблону об успешном добавлении
        request.session['service_added'] = True

        # Перенаправляем на страницу, чтобы избежать повторной отправки формы
        return redirect('service_detail', service_id=service_id)
    else:
        return redirect('main')


def mobile_internet(request):
    services = Service.objects.filter(category='mobile_internet')
    return render(request, 'mainapp/mobile_internet.html', {'services': services})

def wifi(request):
    services = Service.objects.filter(category='wifi')
    return render(request, 'mainapp/wifi.html', {'services': services})

def wifi_tv(request):
    services = Service.objects.filter(category='wifi_tv')
    return render(request, 'mainapp/wifi_tv.html', {'services': services})