from django.test import TestCase

from ..models import Expense, Project


class ProjectTestCase(TestCase):
    def test_str(self):
        project = Project(name="test")
        self.assertEqual(str(project), "test")


class ExpenseTestCase(TestCase):
    def test_str(self):
        expense = Expense(name="test")
        self.assertEqual(str(expense), "test")
