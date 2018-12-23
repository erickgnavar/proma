from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .. import exceptions
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

    def test_finish(self):
        timesheet = Timesheet.objects.create(is_active=True)
        self.assertIsNone(timesheet.date_end)
        timesheet.finish()
        self.assertIsNotNone(timesheet.date_end)
        self.assertFalse(timesheet.is_active)

    def test_clock_in(self):
        qs = Timesheet.objects.filter(is_active=True)
        self.assertEqual(qs.count(), 0)
        Timesheet.clock_in()
        self.assertEqual(qs.count(), 1)

    def test_clock_in_raise_error_when_an_active_timesheet_exists(self):
        qs = Timesheet.objects.filter(is_active=True)
        Timesheet.objects.create(is_active=True)
        self.assertEqual(qs.count(), 1)
        with self.assertRaises(exceptions.ActiveTimesheetExists):
            Timesheet.clock_in()
        self.assertEqual(qs.count(), 1)

    def test_clock_out(self):
        Timesheet.objects.create(is_active=True)
        qs = Timesheet.objects.filter(is_active=True)
        self.assertEqual(qs.count(), 1)
        Timesheet.clock_out()
        self.assertEqual(qs.count(), 0)

    def test_clock_out_raise_error_when_there_is_no_active_timesheet(self):
        qs = Timesheet.objects.filter(is_active=True)
        self.assertEqual(qs.count(), 0)
        with self.assertRaises(exceptions.ActiveTimesheetDoesNotExist):
            Timesheet.clock_out()
        self.assertEqual(qs.count(), 0)
