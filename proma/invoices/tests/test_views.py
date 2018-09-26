from django.contrib.messages.storage.fallback import FallbackStorage
from django.core import mail
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import resolve, reverse
from mixer.backend.django import mixer

from .. import views
from ..models import Invoice


class InvoiceCreateViewTestCase(TestCase):

    def setUp(self):
        self.view = views.InvoiceCreateView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend('users.User')
        self.client = mixer.blend('clients.Client')
        self.project = mixer.blend('projects.Project')

    def test_match_expected_view(self):
        url = resolve('/invoices/create/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context_data)

    def test_create_invoice(self):
        data = {
            'client': self.client.id,
            'project': self.project.id,
            'issue_date': '2018-10-10',
            'due_date': '2018-10-11',
            'items-TOTAL_FORMS': 1,
            'items-INITIAL_FORMS': 0,
            'items-0-description': 'test',
            'items-0-units': 100,
            'items-0-rate': 100,
            'items-0-DELETE': False,
        }
        request = self.factory.post('/', data=data)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        last_invoice = Invoice.objects.last()
        self.assertEqual(last_invoice.items.count(), 1)
        self.assertEqual(response['location'], reverse('invoices:invoice-detail', kwargs={
            'id': last_invoice.id,
        }))

    def test_create_invoice_missing_fields(self):
        data = {
            'client': self.client.id,
        }
        request = self.factory.post('/', data=data)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context_data['form'].errors) > 0)


class InvoiceUpdateViewTestCase(TestCase):

    def setUp(self):
        self.view = views.InvoiceUpdateView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend('users.User')
        self.client = mixer.blend('clients.Client')
        self.project = mixer.blend('projects.Project')
        self.invoice = mixer.blend('invoices.Invoice', client=self.client, project=self.project)

    def test_match_expected_view(self):
        url = resolve('/invoices/1/update/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        request.user = self.user
        response = self.view(request, id=self.invoice.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context_data)

    def test_update_invoice(self):
        another_client = mixer.blend('clients.Client')
        data = {
            'client': another_client.id,
            'project': self.project.id,
            'issue_date': '2018-10-10',
            'due_date': '2018-10-12',
            'items-TOTAL_FORMS': 1,
            'items-INITIAL_FORMS': 0,
            'items-0-description': 'test',
            'items-0-units': 100,
            'items-0-rate': 100,
            'items-0-DELETE': False,
        }
        request = self.factory.post('/', data=data)
        request.user = self.user
        response = self.view(request, id=self.invoice.id)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('invoices:invoice-detail', kwargs={
            'id': self.invoice.id,
        })
        self.assertEqual(response['location'], redirect_url)

    def test_update_invoice_missing_fields(self):
        data = {
            'client': self.client.id,
        }
        request = self.factory.post('/', data=data)
        request.user = self.user
        response = self.view(request, id=self.invoice.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context_data['form'].errors) > 0)

    def test_redirect_when_try_to_edit_a_non_draft_invoice(self):
        request = self.factory.get('/')
        request.user = self.user
        request.session = {}
        request._messages = FallbackStorage(request)
        self.invoice.status = Invoice.OPEN
        self.invoice.save()
        response = self.view(request, id=self.invoice.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], reverse('invoices:invoice-detail', kwargs={
            'id': self.invoice.id,
        }))


class InvoiceListViewTestCase(TestCase):

    def setUp(self):
        self.view = views.InvoiceListView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend('users.User')

    def test_match_expected_view(self):
        url = resolve('/invoices/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        request.user = self.user
        mixer.cycle(5).blend('invoices.Invoice')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('invoices', response.context_data)
        self.assertIn('filter', response.context_data)
        self.assertEqual(response.context_data['invoices'].count(), 5)


class InvoiceDetailViewTestCase(TestCase):

    def setUp(self):
        self.view = views.InvoiceDetailView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend('users.User')
        self.invoice = mixer.blend('invoices.Invoice')

    def test_match_expected_view(self):
        url = resolve('/invoices/1/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        request.user = self.user
        response = self.view(request, id=self.invoice.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn('invoice', response.context_data)


class InvoiceActionViewtTestCase(TestCase):

    def setUp(self):
        self.view = views.InvoiceActionView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend('users.User')
        self.invoice = mixer.blend('invoices.Invoice')

    def test_match_expected_view(self):
        url = resolve('/invoices/1/action/open/')
        self.assertEqual(url.func.__name__, self.view.__name__)
        url = resolve('/invoices/1/action/cancel/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_open_successful(self):
        self.invoice.items.create(rate=10, units=10)
        request = self.factory.get('/')
        request.user = self.user
        request.session = {}
        request._messages = FallbackStorage(request)
        self.assertEqual(self.invoice.status, Invoice.DRAFT)
        self.assertEqual(len(mail.outbox), 0)
        response = self.view(request, id=self.invoice.id, action='open')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], reverse('invoices:invoice-detail', kwargs={
            'id': self.invoice.id,
        }))
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, Invoice.OPEN)

    def test_cancel_successful(self):
        self.invoice.status = Invoice.OPEN
        self.invoice.save()
        request = self.factory.get('/')
        request.user = self.user
        request.session = {}
        request._messages = FallbackStorage(request)
        self.assertEqual(self.invoice.status, Invoice.OPEN)
        response = self.view(request, id=self.invoice.id, action='cancel')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], reverse('invoices:invoice-detail', kwargs={
            'id': self.invoice.id,
        }))
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, Invoice.CANCELLED)


class InvoiceActionPayViewtTestCase(TestCase):

    def setUp(self):
        self.view = views.InvoiceActionPayView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend('users.User')
        self.invoice = mixer.blend('invoices.Invoice', status=Invoice.OPEN)

    def test_match_expected_view(self):
        url = resolve('/invoices/1/action/pay/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_pay_successful(self):
        request = self.factory.post('/', {
            'payment_notes': 'payment notes',
        })
        request.user = self.user
        request.session = {}
        request._messages = FallbackStorage(request)
        self.assertEqual(self.invoice.status, Invoice.OPEN)
        response = self.view(request, id=self.invoice.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], reverse('invoices:invoice-detail', kwargs={
            'id': self.invoice.id,
        }))
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, Invoice.PAID)

    def test_invoice_missing_fields(self):
        data = {}
        request = self.factory.post('/', data=data)
        request.user = self.user
        response = self.view(request, id=self.invoice.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context_data['form'].errors) > 0)

    def test_raise_404_when_the_invoice_is_not_opened(self):
        request = self.factory.post('/')
        request.user = self.user
        self.invoice.status = Invoice.DRAFT
        self.invoice.save()
        with self.assertRaises(Http404):
            self.view(request, id=self.invoice.id)

        request = self.factory.post('/')
        request.user = self.user
        self.invoice.status = Invoice.CANCELLED
        self.invoice.save()
        with self.assertRaises(Http404):
            self.view(request, id=self.invoice.id)


class InvoicePublicDetailViewTestCase(TestCase):

    def setUp(self):
        self.view = views.InvoicePublicDetailView.as_view()
        self.factory = RequestFactory()
        self.invoice = mixer.blend('invoices.Invoice', status=Invoice.OPEN)

    def test_match_expected_view(self):
        url = resolve('/invoices/abc/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        response = self.view(request, token=self.invoice.token)
        self.assertEqual(response.status_code, 200)
        self.assertIn('invoice', response.context_data)

    def test_raise_404_when_the_invoice_is_not_opened(self):
        request = self.factory.get('/')
        self.invoice.status = Invoice.DRAFT
        self.invoice.save()
        with self.assertRaises(Http404):
            self.view(request, token=self.invoice.token)


class InvoiceDownloadPDFViewTestCase(TestCase):

    def setUp(self):
        self.view = views.InvoiceDownloadPDFView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend('users.User')
        self.invoice = mixer.blend('invoices.Invoice', status=Invoice.OPEN)

    def test_match_expected_view(self):
        url = resolve('/invoices/1/download-pdf/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        request.user = self.user
        response = self.view(request, id=self.invoice.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/pdf')

    def test_raise_404_when_the_invoice_is_a_draft(self):
        request = self.factory.get('/')
        request.user = self.user
        self.invoice.status = Invoice.DRAFT
        self.invoice.save()
        with self.assertRaises(Http404):
            self.view(request, id=self.invoice.id)


class InvoiceResendEmailViewTestCase(TestCase):

    def setUp(self):
        self.view = views.InvoiceResendEmailView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend('users.User')
        self.invoice = mixer.blend('invoices.Invoice', status=Invoice.OPEN)

    def test_match_expected_view(self):
        url = resolve('/invoices/1/resend-email/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        request.user = self.user
        request.session = {}
        request._messages = FallbackStorage(request)
        self.assertEqual(len(mail.outbox), 0)
        response = self.view(request, id=self.invoice.id)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('invoices:invoice-detail', kwargs={
            'id': self.invoice.id,
        })
        self.assertEqual(response['location'], redirect_url)

    def test_raise_404_when_the_invoice_is_not_opened(self):
        request = self.factory.get('/')
        request.user = self.user
        self.invoice.status = Invoice.DRAFT
        self.invoice.save()
        with self.assertRaises(Http404):
            self.view(request, id=self.invoice.id)
