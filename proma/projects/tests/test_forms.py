from django.test import TestCase

from .. import forms


class ProjectFormTestCase(TestCase):
    def setUp(self):
        self.form_class = forms.ProjectForm

    def clean_end_date_valid(self):
        form = self.form_class({"start_date": "2018-01-01", "end_date": "2018-01-02"})
        self.assertNotIn("end_date", form.errors)

    def clean_end_date_invalid(self):
        form = self.form_class({"start_date": "2018-01-02", "end_date": "2018-01-01"})
        self.assertIn("end_date", form.errors)
