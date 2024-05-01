from django.shortcuts import render
from .models import Service

# Create your views here.

def main(request):
    services = Service.objects.all()
    return render(request, 'mainapp/main.html', {'services': services})