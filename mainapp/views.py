from django.shortcuts import render
from .models import Service

# Create your views here.

def main(request):
    service = Service.objects.all()
    return render(request, 'mainapp/main.html', {'service': service})