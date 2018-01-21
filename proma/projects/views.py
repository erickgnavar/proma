from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import ExpenseForm, ProjectForm
from .models import Expense, Project


class ProjectCreateView(LoginRequiredMixin, CreateView):

    template_name = 'projects/project_create.html'
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('projects:project-list')


class ProjectUpdateView(LoginRequiredMixin, UpdateView):

    template_name = 'projects/project_update.html'
    model = Project
    context_object_name = 'project'
    form_class = ProjectForm
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('projects:project-detail', kwargs={
            'id': self.object.id,
        })


class ProjectListView(LoginRequiredMixin, ListView):

    template_name = 'projects/project_list.html'
    model = Project
    paginate_by = 20
    context_object_name = 'projects'


class ProjectDetailView(LoginRequiredMixin, DetailView):

    template_name = 'projects/project_detail.html'
    model = Project
    context_object_name = 'project'
    pk_url_kwarg = 'id'


class ExpenseCreateView(LoginRequiredMixin, CreateView):

    template_name = 'projects/expense_create.html'
    model = Expense
    form_class = ExpenseForm
    success_url = reverse_lazy('projects:expense-list')


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):

    template_name = 'projects/expense_update.html'
    model = Expense
    context_object_name = 'expense'
    form_class = ExpenseForm
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
