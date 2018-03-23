from django.test import RequestFactory, TestCase
from django.urls import resolve, reverse
from mixer.backend.django import mixer

from .. import views


class ClientCreateViewTestCase(TestCase):

    def setUp(self):
        self.view = views.ClientCreateView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend('users.User')

    def test_match_expected_view(self):
        url = resolve('/clients/create/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context_data)

    def test_create_client(self):
        data = {
            'name': 'test',
            'email': 'email@email.com',
            'alias': 'test',
        }
        request = self.factory.post('/', data=data)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(reverse('clients:client-list'), response['location'])

    def test_create_client_missing_fields(self):
        data = {
            'name': 'test',
        }
        request = self.factory.post('/', data=data)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context_data['form'].errors) > 0)


class ClientUpdateViewTestCase(TestCase):

    def setUp(self):
        self.view = views.ClientUpdateView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend('users.User')
        self.client = mixer.blend('clients.Client')

    def test_match_expected_view(self):
        url = resolve('/clients/1/update/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        request.user = self.user
        response = self.view(request, id=self.client.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context_data)

    def test_update_client(self):
        data = {
            'name': 'test',
            'email': 'email@email.com',
            'alias': 'test',
        }
        request = self.factory.post('/', data=data)
        request.user = self.user
        response = self.view(request, id=self.client.id)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('clients:client-detail', kwargs={
            'id': self.client.id,
        })
        self.assertEqual(redirect_url, response['location'])

    def test_update_client_missing_fields(self):
        data = {
            'name': 'test',
        }
        request = self.factory.post('/', data=data)
        request.user = self.user
        response = self.view(request, id=self.client.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context_data['form'].errors) > 0)


class ClientListViewTestCase(TestCase):

    def setUp(self):
        self.view = views.ClientListView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend('users.User')

    def test_match_expected_view(self):
        url = resolve('/clients/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        request.user = self.user
        mixer.cycle(5).blend('clients.Client')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('clients', response.context_data)
        self.assertIn('filter', response.context_data)
        self.assertEqual(response.context_data['clients'].count(), 5)


class ClientDetailViewTestCase(TestCase):

    def setUp(self):
        self.view = views.ClientDetailView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend('users.User')
        self.client = mixer.blend('clients.Client')

    def test_match_expected_view(self):
        url = resolve('/clients/1/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        request.user = self.user
        response = self.view(request, id=self.client.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn('client', response.context_data)
