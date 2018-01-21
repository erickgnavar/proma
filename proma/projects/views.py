from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import ProjectForm
from .models import Project


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
