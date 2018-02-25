from django.test import TestCase
from django.utils import timezone
from mixer.backend.django import mixer

from ..exceptions import InvoiceException
from ..models import Invoice, Item


class InvoiceTestCase(TestCase):

    def setUp(self):
        self.client = mixer.blend('clients.Client')
        self.project = mixer.blend('projects.Project')

    def test_str_draft(self):
        invoice = Invoice()
        self.assertEqual(str(invoice), invoice.get_status_display())

    def test_str_no_draft(self):
        invoice = Invoice(status=Invoice.OPEN)
        self.assertNotEqual(str(invoice), invoice.get_status_display())

    def test_compute_totals_no_items(self):
        invoice = Invoice()
        self.assertEqual(invoice.tax_total, 0)
        self.assertEqual(invoice.subtotal, 0)
        self.assertEqual(invoice.total, 0)
        invoice.compute_amounts()
        self.assertEqual(invoice.tax_total, 0)
        self.assertEqual(invoice.subtotal, 0)
        self.assertEqual(invoice.total, 0)

    def test_compute_totals_with_items_no_taxes(self):
        invoice = Invoice.objects.create(
            due_date='2018-01-01',
            client=self.client,
            project=self.project,
        )
        invoice.items.create(
            rate=10,
            units=10,
        )
        self.assertEqual(invoice.tax_total, 0)
        self.assertEqual(invoice.subtotal, 0)
        self.assertEqual(invoice.total, 0)
        invoice.compute_amounts()
        self.assertEqual(invoice.tax_total, 0)
        self.assertEqual(invoice.subtotal, 100)
        self.assertEqual(invoice.total, 100)

    def test_compute_totals_with_items_and_taxes(self):
        invoice = Invoice.objects.create(
            due_date='2018-01-01',
            client=self.client,
            project=self.project,
            tax_percent=10,
        )
        invoice.items.create(
            rate=10,
            units=10,
        )
        self.assertEqual(invoice.tax_total, 0)
        self.assertEqual(invoice.subtotal, 0)
        self.assertEqual(invoice.total, 0)
        invoice.compute_amounts()
        self.assertEqual(invoice.tax_total, 10)
        self.assertEqual(invoice.subtotal, 100)
        self.assertEqual(invoice.total, 110)

    def test_compute_number_draft_invoice(self):
        invoice = Invoice(status=Invoice.DRAFT)
        number = invoice.number
        invoice._compute_number()
        self.assertEqual(invoice.number, number)

    def test_compute_number_no_draft_invoice(self):
        invoice = Invoice()
        # Because the default number is an hex random value
        self.assertEqual(len(invoice.number), 64)
        invoice.status = Invoice.PAID
        invoice._compute_number()
        now = timezone.now()
        number = f'{now.year}00001'
        self.assertEqual(invoice.number, number)

    def test_open(self):
        invoice = Invoice.objects.create(
            due_date='2018-01-01',
            client=self.client,
            project=self.project,
            tax_percent=10,
        )
        invoice.items.create(
            rate=10,
            units=10,
        )
        self.assertEqual(invoice.status, Invoice.DRAFT)
        self.assertIsNone(invoice.opening_date)
        invoice.open()
        self.assertEqual(invoice.status, Invoice.OPEN)
        self.assertIsNotNone(invoice.opening_date)

    def test_open_raise_error_with_no_items(self):
        invoice = Invoice.objects.create(
            due_date='2018-01-01',
            client=self.client,
            project=self.project,
            tax_percent=10,
        )
        with self.assertRaises(InvoiceException):
            invoice.open()

    def test_open_raise_error_for_wrong_status(self):
        invoice = Invoice.objects.create(
            due_date='2018-01-01',
            client=self.client,
            project=self.project,
            tax_percent=10,
            status=Invoice.CANCELLED,
        )
        with self.assertRaises(InvoiceException):
            invoice.open()

    def test_pay(self):
        invoice = Invoice.objects.create(
            due_date='2018-01-01',
            client=self.client,
            project=self.project,
            tax_percent=10,
            status=Invoice.OPEN,
        )
        self.assertEqual(invoice.status, Invoice.OPEN)
        self.assertIsNone(invoice.payment_date)
        invoice.pay()
        self.assertEqual(invoice.status, Invoice.PAID)
        self.assertIsNotNone(invoice.payment_date)

    def test_pay_raise_error_for_wrong_status(self):
        invoice = Invoice.objects.create(
            due_date='2018-01-01',
            client=self.client,
            project=self.project,
            tax_percent=10,
            status=Invoice.DRAFT,
        )
        with self.assertRaises(InvoiceException):
            invoice.pay()

    def test_cancel(self):
        invoice = Invoice.objects.create(
            due_date='2018-01-01',
            client=self.client,
            project=self.project,
            tax_percent=10,
            status=Invoice.OPEN,
        )
        self.assertEqual(invoice.status, Invoice.OPEN)
        self.assertIsNone(invoice.cancellation_date)
        invoice.cancel()
        self.assertEqual(invoice.status, Invoice.CANCELLED)
        self.assertIsNotNone(invoice.cancellation_date)

    def test_cancel_raise_error_for_wrong_status(self):
        invoice = Invoice.objects.create(
            due_date='2018-01-01',
            client=self.client,
            project=self.project,
            tax_percent=10,
            status=Invoice.DRAFT,
        )
        with self.assertRaises(InvoiceException):
            invoice.cancel()


class ItemTestCase(TestCase):

    def setUp(self):
        self.invoice = mixer.blend('invoices.Invoice')

    def test_str(self):
        item = Item(rate=10, units=10, invoice=self.invoice, description='test')
        self.assertEqual(str(item), 'test: 0')

    def test_compute_total_after_save(self):
        item = Item(rate=10, units=10, invoice=self.invoice)
        self.assertEqual(item.total, 0)
        item.save()
        self.assertEqual(item.total, 100)
