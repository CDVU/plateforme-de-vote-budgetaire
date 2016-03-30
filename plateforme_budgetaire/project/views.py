from django.shortcuts import render
from django.views import generic
from project.models import Project, SubProject, PROJECT_STATUS_CHOICES
from project.forms import ProjectsForm
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect


class ProjectDetail(generic.DetailView):
    # List all project
    model = Project
    template_name = 'project/project_detail.html'

    def dispatch(self, *args, **kwargs):
        print kwargs['pk']
        return super(ProjectDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        for key, value in PROJECT_STATUS_CHOICES:
            if key == self.object.status:
                context['status_id'] = value

        context['sub_projects'] = SubProject.objects.filter(project=self.object)
        return context


class ProjectList(generic.ListView):
    # List all project
    template_name = 'project/project_list.html'
    context_object_name = 'projects'

    def dispatch(self, *args, **kwargs):
        if self.kwargs['validated'] != 'all':
            self.status = int(self.kwargs['validated'])
        else:
            self.status = 'all'
        return super(ProjectList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        if self.status == 'all':
            return Project.objects.all().order_by('-date_of_submission')
        else:
            status = PROJECT_STATUS_CHOICES[self.status][0]
            return Project.objects.filter(status=status).order_by('-date_of_submission')

    def get_context_data(self, **kwargs):
        context = super(ProjectList, self).get_context_data(**kwargs)
        context['validation_state_selected'] = self.status
        context['status_list'] = PROJECT_STATUS_CHOICES
        return context


class ProjectCreate(generic.CreateView):
    form_class = ProjectsForm
    template_name = 'project/project_form.html'

    def dispatch(self, *args, **kwargs):
        return super(ProjectCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.status = PROJECT_STATUS_CHOICES[0][0]
        return super(ProjectCreate, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


def accept_project(request, id_of_project):
    project = Project.objects.get(id=id_of_project)
    project.status = PROJECT_STATUS_CHOICES[1][0]
    project.save(update_fields=['status'])

    return redirect(reverse_lazy("projects:project_detail", args=[project.id]))


def refuse_project(request, id_of_project):
    project = Project.objects.get(id=id_of_project)
    project.status = PROJECT_STATUS_CHOICES[2][0]
    project.save(update_fields=['status'])

    return redirect(reverse_lazy("projects:project_detail", args=[project.id]))
