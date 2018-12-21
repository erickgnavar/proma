from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic import UpdateView

from .forms import ConfigurationForm
from .models import Configuration


class ConfigurationUpdateView(LoginRequiredMixin, UpdateView):

    template_name = "config/configuration_update.html"
    model = Configuration
    form_class = ConfigurationForm

    def get_object(self):
        return Configuration.get_instance()

    def get_success_url(self):
        messages.success(self.request, _("Configuration saved!"))
        return reverse("config:configuration-update")
