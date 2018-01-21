from django.test import RequestFactory, TestCase
from django.urls import resolve, reverse
from mixer.backend.django import mixer

from .. import views
from ..models import Project


class ProjectCreateViewTestCase(TestCase):

    def setUp(self):
        self.view = views.ProjectCreateView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend('users.User')

    def test_match_expected_view(self):
        url = resolve('/projects/create/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context_data)

    def test_create_project(self):
        client = mixer.blend('clients.Client')
        data = {
            'name': 'test',
            'client': client.id,
            'start_date': '2018-01-01',
            'payment_type': Project.FLAT_RATE,
            'currency': Project.USD,
            'rate': 20,
        }
        request = self.factory.post('/', data=data)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(reverse('projects:project-list'), response['location'])

    def test_create_project_missing_fields(self):
        data = {
            'name': 'test',
        }
        request = self.factory.post('/', data=data)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context_data['form'].errors) > 0)


class ProjectUpdateViewTestCase(TestCase):

    def setUp(self):
        self.view = views.ProjectUpdateView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend('users.User')
        self.project = mixer.blend('projects.Project')

    def test_match_expected_view(self):
        url = resolve('/projects/1/update/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        request.user = self.user
        response = self.view(request, id=self.project.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context_data)

    def test_update_project(self):
        data = {
            'name': 'test',
            'client': self.project.client.id,
            'start_date': '2018-01-01',
            'payment_type': Project.DAILY_RATE,
            'currency': Project.USD,
            'rate': 20,
        }
        request = self.factory.post('/', data=data)
        request.user = self.user
        response = self.view(request, id=self.project.id)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('projects:project-detail', kwargs={
            'id': self.project.id,
        })
        self.project.refresh_from_db()
        self.assertEqual(self.project.payment_type, Project.DAILY_RATE)
        self.assertEqual(redirect_url, response['location'])

    def test_update_project_missing_fields(self):
        data = {
            'name': 'test',
        }
        request = self.factory.post('/', data=data)
        request.user = self.user
        response = self.view(request, id=self.project.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context_data['form'].errors) > 0)


class ProjectListViewTestCase(TestCase):

    def setUp(self):
        self.view = views.ProjectListView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend('users.User')

    def test_match_expected_view(self):
        url = resolve('/projects/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        request.user = self.user
        mixer.cycle(5).blend('projects.Project')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('projects', response.context_data)
        self.assertEqual(response.context_data['projects'].count(), 5)


class ProjectDetailViewTestCase(TestCase):

    def setUp(self):
        self.view = views.ProjectDetailView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend('users.User')
        self.project = mixer.blend('projects.Project')

    def test_match_expected_view(self):
        url = resolve('/projects/1/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        request.user = self.user
        response = self.view(request, id=self.project.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn('project', response.context_data)
