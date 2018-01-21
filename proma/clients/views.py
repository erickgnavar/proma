from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import ClientForm
from .models import Client


class ClientCreateView(LoginRequiredMixin, CreateView):

    template_name = 'clients/client_create.html'
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('clients:client-list')


class ClientUpdateView(LoginRequiredMixin, UpdateView):

    template_name = 'clients/client_update.html'
    model = Client
    context_object_name = 'client'
    form_class = ClientForm
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('clients:client-detail', kwargs={
            'id': self.object.id,
        })


class ClientListView(LoginRequiredMixin, ListView):

    template_name = 'clients/client_list.html'
    model = Client
    paginate_by = 20
    context_object_name = 'clients'


class ClientDetailView(LoginRequiredMixin, DetailView):

    template_name = 'clients/client_detail.html'
    model = Client
    context_object_name = 'client'
    pk_url_kwarg = 'id'
