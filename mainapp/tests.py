from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import UserProfile, Service
from django.urls import reverse


class UserProfileViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        # Создаем пользователя
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password'
        )
        # Создаем профиль пользователя
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            phone_number='+996708711708',
            address='Дом'
        )

    def test_user_profile_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'test@example.com')
        self.assertContains(response, '+996708711708')
        self.assertContains(response, 'Дом')




class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_view(self):
        # Подготовка данных для отправки POST-запроса
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            'phone_number': '+123456789',
            'address': 'Test Address'
        }

        # Отправка POST-запроса на страницу регистрации
        response = self.client.post(reverse('register'), data)

        # Проверка, что пользователь был успешно создан и перенаправлен на страницу входа
        self.assertEqual(response.status_code, 302)  # Перенаправление
        self.assertTrue(User.objects.filter(username='testuser').exists())  # Проверка создания пользователя


class AddRequestViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Создаем пользователя
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        # Создаем профиль пользователя
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            phone_number='+123456789',
            address='Test Address'
        )
        # Создаем услугу
        self.service = Service.objects.create(
            name='Test Service',
            category='mobile_internet',
            description='Test Description',
            price=100
        )

    def test_add_request_view(self):
        # Аутентификация пользователя
        self.client.login(username='testuser', password='testpassword')

        # Отправляем POST-запрос на страницу добавления заявки
        response = self.client.post(reverse('add_request'), {'service_id': self.service.id})

        # Проверяем, что заявка была успешно добавлена и происходит перенаправление на страницу деталей услуги
        self.assertEqual(response.status_code, 302)  # Перенаправление
        self.assertTrue(self.user_profile.services.filter(id=self.service.id).exists())  # Проверка добавления заявки


class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Создаем пользователя
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        # Создаем профиль пользователя
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            phone_number='+123456789',
            address='Test Address'
        )
        # Создаем услуги
        self.service1 = Service.objects.create(
            name='Test Service 1',
            category='mobile_internet',
            description='Test Description 1',
            price=100
        )
        self.service2 = Service.objects.create(
            name='Test Service 2',
            category='wifi',
            description='Test Description 2',
            price=200
        )
        # Добавляем заявки на услуги для пользователя
        self.user_profile.services.add(self.service1)
        self.user_profile.services.add(self.service2)

    def test_profile_view(self):
        # Аутентификация пользователя
        self.client.login(username='testuser', password='testpassword')

        # Отправляем GET-запрос на страницу профиля пользователя
        response = self.client.get(reverse('profile'))

        # Проверяем, что страница отображается корректно и содержит информацию о пользователе и его заявках на услуги
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')  # Проверка имени пользователя
        self.assertContains(response, '+123456789')  # Проверка номера телефона
        self.assertContains(response, 'Test Address')  # Проверка адреса
        self.assertContains(response, 'Test Service 1')  # Проверка наличия заявки на первую услугу
        self.assertContains(response, 'Test Service 2')  # Проверка наличия заявки на вторую услугу


class ServiceDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Создаем тестовую услугу
        self.service = Service.objects.create(
            name='Test Service',
            category='mobile_internet',
            description='Test Description',
            price=100
        )

    def test_service_detail_view(self):
        # Отправляем GET-запрос на страницу деталей услуги
        response = self.client.get(reverse('service_detail', args=[self.service.id]))

        # Проверяем, что страница отображается корректно и содержит информацию о выбранной услуге
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Service')  # Проверка имени услуги
        self.assertContains(response, 'Test Description')  # Проверка описания услуги
        self.assertContains(response, '100')  # Проверка цены услуги