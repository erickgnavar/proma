from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from proma.clients.models import Client
from proma.projects.models import Expense, Project


class HomeView(LoginRequiredMixin, TemplateView):

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'projects_quantity': Project.objects.count(),
            'expenses_quantity': Expense.objects.count(),
            'clients_quantity': Client.objects.count(),
        })
        return context