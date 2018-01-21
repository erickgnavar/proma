from django.test import TestCase

from ..models import Project


class ProjectTestCase(TestCase):

    def test_str(self):
        project = Project(name='test')
        self.assertEqual(str(project), 'test')
