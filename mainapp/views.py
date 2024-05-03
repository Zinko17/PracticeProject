from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Service, UserProfile
from .forms import UserProfileForm, UserForm, RegistrationForm

# Create your views here.

def main(request):
    services = Service.objects.all()
    return render(request, 'mainapp/main.html', {'services': services})

@login_required
def profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'mainapp/profile.html', {'userprofile': user_profile})

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
