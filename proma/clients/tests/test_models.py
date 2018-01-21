from django.test import TestCase

from ..models import Client


class ClientTestCase(TestCase):

    def test_str(self):
        client = Client(name='test')
        self.assertEqual(str(client), 'test')
