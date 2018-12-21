from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase
from django.urls import resolve, reverse
from mixer.backend.django import mixer

from .. import views
from ..models import Configuration


class ConfigurationUpdateViewTestCase(TestCase):
    def setUp(self):
        self.view = views.ConfigurationUpdateView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend("users.User")
        self.configuration = Configuration.get_instance()

    def test_match_expected_view(self):
        url = resolve("/settings/")
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get("/")
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context_data)

    def test_update_configuration(self):
        data = {"legal_name": "test"}
        request = self.factory.post("/", data=data)
        request.user = self.user
        request.session = {}
        request._messages = FallbackStorage(request)
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse("config:configuration-update")
        self.assertEqual(redirect_url, response["location"])
