from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase
from django.urls import resolve, reverse
from mixer.backend.django import mixer

from .. import forms, views
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
        self.assertIn('filter', response.context_data)
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


class ExpenseCreateViewTestCase(TestCase):

    def setUp(self):
        self.view = views.ExpenseCreateView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend('users.User')

    def test_match_expected_view(self):
        url = resolve('/expenses/create/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context_data)

    def test_create_expense(self):
        project = mixer.blend('projects.Project')
        data = {
            'name': 'test',
            'project': project.id,
            'date': '2018-01-01',
            'amount': 10.00,
        }
        request = self.factory.post('/', data=data)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(reverse('projects:expense-list'), response['location'])

    def test_create_expense_missing_fields(self):
        data = {
            'name': 'test',
        }
        request = self.factory.post('/', data=data)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context_data['form'].errors) > 0)


class ExpenseUpdateViewTestCase(TestCase):

    def setUp(self):
        self.view = views.ExpenseUpdateView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend('users.User')
        self.expense = mixer.blend('projects.Expense')

    def test_match_expected_view(self):
        url = resolve('/expenses/1/update/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        request.user = self.user
        response = self.view(request, id=self.expense.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context_data)

    def test_update_expense(self):
        data = {
            'name': 'another name',
            'project': self.expense.project.id,
            'date': '2018-01-01',
            'amount': 20,
        }
        request = self.factory.post('/', data=data)
        request.user = self.user
        response = self.view(request, id=self.expense.id)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('projects:expense-detail', kwargs={
            'id': self.expense.id,
        })
        self.expense.refresh_from_db()
        self.assertEqual(self.expense.name, 'another name')
        self.assertEqual(redirect_url, response['location'])

    def test_update_expense_missing_fields(self):
        data = {
            'name': 'test',
        }
        request = self.factory.post('/', data=data)
        request.user = self.user
        response = self.view(request, id=self.expense.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context_data['form'].errors) > 0)


class ExpenseListViewTestCase(TestCase):

    def setUp(self):
        self.view = views.ExpenseListView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend('users.User')

    def test_match_expected_view(self):
        url = resolve('/expenses/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        request.user = self.user
        mixer.cycle(5).blend('projects.Expense')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('expenses', response.context_data)
        self.assertIn('filter', response.context_data)
        self.assertEqual(response.context_data['expenses'].count(), 5)


class ExpenseDetailViewTestCase(TestCase):

    def setUp(self):
        self.view = views.ExpenseDetailView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend('users.User')
        self.expense = mixer.blend('projects.Expense')

    def test_match_expected_view(self):
        url = resolve('/expenses/1/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        request.user = self.user
        response = self.view(request, id=self.expense.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn('expense', response.context_data)


class ProjectCreateInvoiceViewTestCase(TestCase):

    def setUp(self):
        self.view = views.ProjectCreateInvoiceView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend('users.User')
        self.project = mixer.blend('projects.Project')

    def test_match_expected_view(self):
        url = resolve('/projects/1/create-invoice/flat/')
        self.assertEqual(url.func.__name__, self.view.__name__)
        url = resolve('/projects/1/create-invoice/rate/')
        self.assertEqual(url.func.__name__, self.view.__name__)
        url = resolve('/projects/1/create-invoice/percentage/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_flat_form(self):
        request = self.factory.get('/')
        request.user = self.user
        response = self.view(request, id=self.project.id, type='flat')
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context_data)
        self.assertIsInstance(response.context_data['form'], forms.CreateInvoiceFlatForm)

    def test_load_rate_form(self):
        request = self.factory.get('/')
        request.user = self.user
        response = self.view(request, id=self.project.id, type='rate')
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context_data)
        self.assertIsInstance(response.context_data['form'], forms.CreateInvoiceRateForm)

    def test_load_percentage_form(self):
        request = self.factory.get('/')
        request.user = self.user
        response = self.view(request, id=self.project.id, type='percentage')
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context_data)
        self.assertIsInstance(response.context_data['form'], forms.CreateInvoicePercentageForm)

    def test_create_invoice_flat(self):
        request = self.factory.post('/', {
            'description': 'test',
            'amount': 10,
        })
        request.user = self.user
        request.session = {}
        request._messages = FallbackStorage(request)
        invoice = self.project.invoices.last()
        self.assertIsNone(invoice)
        response = self.view(request, id=self.project.id, type='flat')
        self.assertEqual(response.status_code, 302)
        invoice = self.project.invoices.last()
        self.assertIsNotNone(invoice)
        self.assertEqual(response['location'], reverse('invoices:invoice-detail', kwargs={
            'id': invoice.id,
        }))

    def test_create_invoice_rate(self):
        request = self.factory.post('/', {
            'description': 'test',
            'rate': 10,
            'units': 10,
        })
        request.user = self.user
        request.session = {}
        request._messages = FallbackStorage(request)
        invoice = self.project.invoices.last()
        self.assertIsNone(invoice)
        response = self.view(request, id=self.project.id, type='rate')
        self.assertEqual(response.status_code, 302)
        invoice = self.project.invoices.last()
        self.assertIsNotNone(invoice)
        self.assertEqual(response['location'], reverse('invoices:invoice-detail', kwargs={
            'id': invoice.id,
        }))

    def test_create_invoice_percentage(self):
        request = self.factory.post('/', {
            'description': 'test',
            'percentage': 10,
        })
        request.user = self.user
        request.session = {}
        request._messages = FallbackStorage(request)
        invoice = self.project.invoices.last()
        self.assertIsNone(invoice)
        response = self.view(request, id=self.project.id, type='percentage')
        self.assertEqual(response.status_code, 302)
        invoice = self.project.invoices.last()
        self.assertIsNotNone(invoice)
        self.assertEqual(response['location'], reverse('invoices:invoice-detail', kwargs={
            'id': invoice.id,
        }))
