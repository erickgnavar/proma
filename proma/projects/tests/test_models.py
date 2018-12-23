from django.test import TestCase
from datetime import timedelta
from django.utils import timezone

from ..models import Expense, Project, Timesheet


class ProjectTestCase(TestCase):
    def test_str(self):
        project = Project(name="test")
        self.assertEqual(str(project), "test")


class ExpenseTestCase(TestCase):
    def test_str(self):
        expense = Expense(name="test")
        self.assertEqual(str(expense), "test")


class TimesheetTestCase(TestCase):
    def test_str(self):
        timesheet = Timesheet(label="test")
        self.assertEqual(str(timesheet), "test")

    def test_diff(self):
        date_start = timezone.now()
        date_end = date_start + timedelta(hours=1)
        timesheet = Timesheet(date_start=date_start, date_end=date_end)
        self.assertEqual(timesheet.diff, date_end - date_start)

    def test_diff_return_none_with_no_date_end(self):
        date_start = timezone.now()
        timesheet = Timesheet(date_start=date_start, date_end=None)
        self.assertEqual(timesheet.diff, None)

    def test_diff_humanize(self):
        date_start = timezone.now()
        date_end = date_start + timedelta(hours=1)
        timesheet = Timesheet(date_start=date_start, date_end=date_end)
        self.assertEqual(timesheet.diff_humanize, "1 hour")

    def test_diff_humanize_return_empty_string_with_no_date_end(self):
        date_start = timezone.now()
        timesheet = Timesheet(date_start=date_start, date_end=None)
        self.assertEqual(timesheet.diff_humanize, "")
