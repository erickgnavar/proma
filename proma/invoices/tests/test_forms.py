from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from ..forms import InvoiceForm


class InvoiceFormTestCase(TestCase):
    def setUp(self):
        self.form_class = InvoiceForm

    def test_clean_due_date_valid_data(self):
        now = timezone.now()
        data = {"issue_date": now, "due_date": now + timedelta(days=1)}
        form = self.form_class(data)
        form.is_valid()
        self.assertNotIn("due_date", form.errors)

    def test_clean_due_date_invalid_data_same_issue_date(self):
        now = timezone.now()
        data = {"issue_date": now, "due_date": now}
        form = self.form_class(data)
        form.is_valid()
        self.assertIn("due_date", form.errors)

    def test_clean_due_date_invalid_data_due_date_is_earlier_than_issue_date(self):
        now = timezone.now()
        data = {"issue_date": now, "due_date": now - timedelta(days=1)}
        form = self.form_class(data)
        form.is_valid()
        self.assertIn("due_date", form.errors)
