from django.contrib.auth.models import User
from django.db import models

class Service(models.Model):
    CATEGORY_CHOICES = (
        ('mobile_internet', 'Мобильный интернет'),
        ('wifi', 'Wi-Fi'),
        ('wifi_tv', 'Wi-Fi + ТВ'),
    )
    name = models.CharField('Название', max_length=100)
    category = models.CharField('Категория', max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField('Описание услуги')
    price = models.IntegerField('Цена услуги')

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, blank=True)
    phone_number = models.CharField('Номер телефона', max_length=15)
    address = models.CharField('Адрес', max_length=50)

    def __str__(self):
        return self.user.username
