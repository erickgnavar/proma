from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from proma.clients.models import Client
from proma.invoices.models import Invoice
from proma.projects.models import Expense, Project


class HomeView(LoginRequiredMixin, TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        latest_invoices = (
            Invoice.objects.exclude(status__in=(Invoice.DRAFT, Invoice.CANCELLED))
            .select_related("client")
            .order_by("-issue_date")
        )[:6]

        context.update(
            {
                "projects_quantity": Project.objects.count(),
                "expenses_quantity": Expense.objects.count(),
                "clients_quantity": Client.objects.count(),
                "invoices_quantity": Invoice.objects.count(),
                "latest_invoices": latest_invoices,
                "invoices_summary": Invoice.summary(),
            }
        )
        return context
