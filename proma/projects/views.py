from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    RedirectView,
    UpdateView,
)
from django_filters.views import FilterView

from proma.invoices.models import Invoice

from . import exceptions, filters, forms
from .models import Expense, Project, Timesheet


class ProjectCreateView(LoginRequiredMixin, CreateView):

    template_name = "projects/project_create.html"
    model = Project
    form_class = forms.ProjectForm
    success_url = reverse_lazy("projects:project-list")


class ProjectUpdateView(LoginRequiredMixin, UpdateView):

    template_name = "projects/project_update.html"
    model = Project
    context_object_name = "project"
    form_class = forms.ProjectForm
    pk_url_kwarg = "id"

    def get_success_url(self):
        return reverse("projects:project-detail", kwargs={"id": self.object.id})


class ProjectCreateInvoiceView(LoginRequiredMixin, FormView):

    template_name = "projects/project_create_invoice.html"

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, id=kwargs.get("id"))
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        # the possible values of type are validated in the url regex
        form_class = {
            "flat": forms.CreateInvoiceFlatForm,
            "rate": forms.CreateInvoiceRateForm,
            "percentage": forms.CreateInvoicePercentageForm,
        }
        return form_class[self.kwargs.get("type")]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"project": self.project})
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"project": self.project})
        return kwargs

    def form_valid(self, form):
        self.invoice = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Draft invoice created!"))
        return reverse("invoices:invoice-detail", kwargs={"id": self.invoice.id})


class ProjectListView(LoginRequiredMixin, FilterView):

    template_name = "projects/project_list.html"
    model = Project
    paginate_by = settings.PAGINATION_DEFAULT_PAGE_SIZE
    context_object_name = "projects"
    filterset_class = filters.ProjectFilter

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(expenses_amount=Sum("expenses__amount"))
        paid_invoice = Q(invoices__status=Invoice.PAID)
        qs = qs.annotate(total_paid=Sum("invoices__total", filter=paid_invoice))
        return qs


class ProjectDetailView(LoginRequiredMixin, DetailView):

    template_name = "projects/project_detail.html"
    model = Project
    context_object_name = "project"
    pk_url_kwarg = "id"


class ExpenseCreateView(LoginRequiredMixin, CreateView):

    template_name = "projects/expense_create.html"
    model = Expense
    form_class = forms.ExpenseForm
    success_url = reverse_lazy("projects:expense-list")


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):

    template_name = "projects/expense_update.html"
    model = Expense
    context_object_name = "expense"
    form_class = forms.ExpenseForm
    pk_url_kwarg = "id"

    def get_success_url(self):
        return reverse("projects:expense-detail", kwargs={"id": self.object.id})


class ExpenseListView(LoginRequiredMixin, FilterView):

    template_name = "projects/expense_list.html"
    model = Expense
    paginate_by = settings.PAGINATION_DEFAULT_PAGE_SIZE
    context_object_name = "expenses"
    filterset_class = filters.ExpenseFilter


class ExpenseDetailView(LoginRequiredMixin, DetailView):

    template_name = "projects/expense_detail.html"
    model = Expense
    context_object_name = "expense"
    pk_url_kwarg = "id"


class TimesheetListView(LoginRequiredMixin, FilterView):

    template_name = "projects/timesheet_list.html"
    model = Timesheet
    paginate_by = settings.PAGINATION_DEFAULT_PAGE_SIZE
    context_object_name = "timesheets"
    filterset_class = filters.TimesheetFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"assign_project_form": forms.AssignProjectToTimesheetsForm()})
        return context

    def post(self, request, *args, **kwargs):
        # TODO: move this to an external view
        form = forms.AssignProjectToTimesheetsForm(request.POST or None)
        if form.is_valid():
            form.process()
            messages.success(request, _("The assignment was successful"))
        else:
            messages.warning(request, _("Project assignment failed, try again"))
        return redirect("projects:timesheet-list")


class TimesheetCreateView(LoginRequiredMixin, CreateView):

    template_name = "projects/timesheet_create.html"
    model = Timesheet
    form_class = forms.TimesheetForm
    success_url = reverse_lazy("projects:timesheet-list")


class TimesheetUpdateView(LoginRequiredMixin, UpdateView):

    template_name = "projects/timesheet_update.html"
    model = Timesheet
    context_object_name = "timesheet"
    form_class = forms.TimesheetForm
    pk_url_kwarg = "id"

    def get_success_url(self):
        return reverse("projects:timesheet-detail", kwargs={"id": self.object.id})


class TimesheetDetailView(LoginRequiredMixin, DetailView):

    template_name = "projects/timesheet_detail.html"
    model = Timesheet
    context_object_name = "timesheet"
    pk_url_kwarg = "id"


class TimesheetClockInView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, **kwargs):
        redirect_url = self.request.META.get("HTTP_REFERER", reverse("home"))
        try:
            Timesheet.clock_in()
        except exceptions.ActiveTimesheetExists:
            messages.warning(self.request, _("There is already an active timesheet"))
        return redirect_url


class TimesheetClockOutView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, **kwargs):
        redirect_url = self.request.META.get("HTTP_REFERER", reverse("home"))
        try:
            Timesheet.clock_out()
        except exceptions.ActiveTimesheetDoesNotExist:
            messages.warning(self.request, _("There is not active timesheet"))
        return redirect_url
