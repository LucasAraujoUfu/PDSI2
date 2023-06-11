from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.backends.db import SessionStore
from mysite.views import home, dados, login, consulta, train, train_db, ia
from mysite.models import dataset


class home_test(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_home_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mysite/home.html')


class view_dados_test(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_dados_view_with_file(self):
        url = reverse('dados')
        request = self.factory.post(url, data={}, files={'arq': open('/home/lucas/Documentos/pdsi2/pdsi/mysite/tests/tests_datasets/datasetFinal.csv', 'rb')})
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = dados(request)
        self.assertEqual(response.status_code, 200)

    def test_dados_view_without_file(self):
        url = reverse('dados')
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)


class view_login_test(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_view_with_valid_credentials(self):
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpassword'}
        request = self.factory.post(url, data=data)
        request.user = self.user
        request.session = SessionStore()
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = login(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '../')

    def test_login_view_with_invalid_credentials(self):
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mysite/login.html')
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Usuário ou senha inválidos')


class view_consulta_test(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_consulta_view_with_authenticated_user_and_trained_model(self):
        self.client.login(username='testuser', password='testpass')
        # TODO: dar um fit em IA
        response = self.client.get('/consulta/')
        self.assertEqual(response.status_code, 302)

    def test_consulta_view_with_authenticated_user_and_untrained_model(self):
        url = reverse('consulta')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_consulta_view_with_unauthenticated_user(self):
        url = reverse('consulta')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


# class view_train_test(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#
#     def test_train_view_with_authenticated_user_and_data(self):
#         url = reverse('train')  # O nome da URL da view 'train'
#         data = {'data': 'ok'}
#         request = self.client.get(url, data=data)
#         request.user = self.user
#         setattr(request, 'session', 'session')
#         messages = FallbackStorage(request)
#         setattr(request, '_messages', messages)
#         response = train(request)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'mysite/train.html')
#         self.assertEqual(response.context['data'], 'ok')
#
#     def test_train_view_with_authenticated_user_and_no_data(self):
#         url = reverse('train')
#         request = self.factory.get(url)
#         request.user = self.user
#         setattr(request, 'session', 'session')
#         messages = FallbackStorage(request)
#         setattr(request, '_messages', messages)
#         response = train(request)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'mysite/train.html')
#         self.assertNotIn('data', response.context)
#
#     def test_train_view_with_unauthenticated_user(self):
#         url = reverse('train')
#         request = self.factory.get(url)
#         setattr(request, 'session', 'session')
#         messages = FallbackStorage(request)
#         setattr(request, '_messages', messages)
#         response = train(request)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, '/login/?next=/train/')


# class view_train_db_test(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#
#     def test_train_db_view_with_authenticated_user(self):
#         url = reverse('train_db')
#         request = self.factory.get(url)
#         request.user = self.user
#         response = train_db(request)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'mysite/dados.html')
#         self.assertIn('cols', response.context)
#         self.assertIn('dados', response.context)
