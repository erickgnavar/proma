from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import (CreateView, DetailView, ListView,
                                  RedirectView, UpdateView)

from .exceptions import InvoiceException
from .forms import InvoiceForm, ItemsFormset
from .models import Invoice


class InvoiceCreateView(LoginRequiredMixin, CreateView):

    template_name = 'invoices/invoice_create.html'
    model = Invoice
    form_class = InvoiceForm
    success_url = reverse_lazy('invoices:invoice-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items_formset'] = ItemsFormset(self.request.POST or None)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context['items_formset']
        if form.is_valid() and items_formset.is_valid():
            invoice = form.save()
            items_formset.instance = invoice
            items_formset.save()
            invoice = form.save(commit=False)
            invoice.compute_amounts()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('invoices:invoice-detail', kwargs={
            'id': self.object.id,
        })


class InvoiceUpdateView(LoginRequiredMixin, UpdateView):

    template_name = 'invoices/invoice_update.html'
    model = Invoice
    context_object_name = 'invoice'
    form_class = InvoiceForm
    pk_url_kwarg = 'id'

    def dispatch(self, request, *args, **kwargs):
        invoice = self.get_object()
        if invoice.can_be_edited:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, _("The invoice can't be edited"))
            return redirect('invoices:invoice-detail', id=invoice.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items_formset'] = ItemsFormset(self.request.POST or None, instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context['items_formset']
        if form.is_valid() and items_formset.is_valid():
            items_formset.save()
            invoice = form.save(commit=False)
            invoice.compute_amounts()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('invoices:invoice-detail', kwargs={
            'id': self.object.id,
        })


class InvoiceListView(LoginRequiredMixin, ListView):

    template_name = 'invoices/invoice_list.html'
    model = Invoice
    paginate_by = 20
    context_object_name = 'invoices'


class InvoiceDetailView(LoginRequiredMixin, DetailView):

    template_name = 'invoices/invoice_detail.html'
    model = Invoice
    context_object_name = 'invoice'
    pk_url_kwarg = 'id'


class InvoiceActionView(LoginRequiredMixin, RedirectView):

    def dispatch(self, request, *args, **kwargs):
        self.invoice = get_object_or_404(Invoice, id=kwargs.get('id'))
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        action = kwargs.get('action')
        if action == 'open':
            try:
                self.invoice.open()
                self.invoice.save()
                messages.success(self.request, _('Invoice opened!'))
            except InvoiceException as ex:
                messages.error(self.request, str(ex))
        elif action == 'cancel':
            try:
                self.invoice.cancel()
                self.invoice.save()
                messages.success(self.request, _('Invoice canceled!'))
            except InvoiceException as ex:
                messages.error(self.request, str(ex))
        return reverse('invoices:invoice-detail', kwargs={
            'id': self.invoice.id,
        })