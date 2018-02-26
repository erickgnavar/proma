from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  UpdateView)

from . import forms
from .models import Expense, Project


class ProjectCreateView(LoginRequiredMixin, CreateView):

    template_name = 'projects/project_create.html'
    model = Project
    form_class = forms.ProjectForm
    success_url = reverse_lazy('projects:project-list')


class ProjectUpdateView(LoginRequiredMixin, UpdateView):

    template_name = 'projects/project_update.html'
    model = Project
    context_object_name = 'project'
    form_class = forms.ProjectForm
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('projects:project-detail', kwargs={
            'id': self.object.id,
        })


class ProjectCreateInvoiceView(LoginRequiredMixin, FormView):

    template_name = 'projects/project_create_invoice.html'

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, id=kwargs.get('id'))
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        # the possible values of type are validated in the url regex
        form_class = {
            'flat': forms.CreateInvoiceFlatForm,
            'rate': forms.CreateInvoiceRateForm,
            'percentage': forms.CreateInvoicePercentageForm,
        }
        return form_class[self.kwargs.get('type')]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'project': self.project,
        })
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'project': self.project
        })
        return kwargs

    def form_valid(self, form):
        self.invoice = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _('Draft invoice created!'))
        return reverse('invoices:invoice-detail', kwargs={
            'id': self.invoice.id,
        })


class ProjectListView(LoginRequiredMixin, ListView):

    template_name = 'projects/project_list.html'
    model = Project
    paginate_by = 20
    context_object_name = 'projects'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(expenses_amount=Sum('expenses__amount'))
        return qs


class ProjectDetailView(LoginRequiredMixin, DetailView):

    template_name = 'projects/project_detail.html'
    model = Project
    context_object_name = 'project'
    pk_url_kwarg = 'id'


class ExpenseCreateView(LoginRequiredMixin, CreateView):

    template_name = 'projects/expense_create.html'
    model = Expense
    form_class = forms.ExpenseForm
    success_url = reverse_lazy('projects:expense-list')


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):

    template_name = 'projects/expense_update.html'
    model = Expense
    context_object_name = 'expense'
    form_class = forms.ExpenseForm
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('projects:expense-detail', kwargs={
            'id': self.object.id,
        })


class ExpenseListView(LoginRequiredMixin, ListView):

    template_name = 'projects/expense_list.html'
    model = Expense
    paginate_by = 20
    context_object_name = 'expenses'


class ExpenseDetailView(LoginRequiredMixin, DetailView):

    template_name = 'projects/expense_detail.html'
    model = Expense
    context_object_name = 'expense'
    pk_url_kwarg = 'id'
