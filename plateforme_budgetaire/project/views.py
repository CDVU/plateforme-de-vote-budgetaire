# coding: utf-8

from django.views import generic
from project.models import Project, SubProject, PROJECT_STATUS_CHOICES
from project.forms import ProjectsForm, SubProjectsForm
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404


class ProjectDetail(generic.DetailView):
    # List all project
    model = Project
    template_name = 'project/project_detail.html'

    def dispatch(self, *args, **kwargs):
        return super(ProjectDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        for key, value in PROJECT_STATUS_CHOICES:
            if key == self.object.status:
                context['status_id'] = value

        context['sub_projects'] = SubProject.objects.\
            filter(project=self.object)
        return context


class ProjectList(generic.ListView):
    # List all project
    template_name = 'project/project_list.html'
    context_object_name = 'projects'

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        if self.kwargs['validated'] != 'all':
            self.status = int(self.kwargs['validated'])
        else:
            self.status = 'all'
        return super(ProjectList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_staff:
            if self.status == 'all':
                list_project = Project.objects.all().\
                    order_by('-date_of_submission')
            else:
                status = PROJECT_STATUS_CHOICES[self.status][0]
                list_project = Project.objects.filter(
                    status=status
                ).order_by('-date_of_submission')
        else:
            if self.status == 'all':
                list_project = Project.objects.filter(
                    creator=self.request.user
                ).order_by('-date_of_submission')
            else:
                status = PROJECT_STATUS_CHOICES[self.status][0]
                list_project = Project.objects.filter(
                    status=status,
                    creator=self.request.user
                ).order_by('-date_of_submission')

        return list_project

    def get_context_data(self, **kwargs):
        context = super(ProjectList, self).get_context_data(**kwargs)
        context['validation_state_selected'] = self.status
        context['status_list'] = PROJECT_STATUS_CHOICES
        return context


class ProjectCreate(generic.CreateView):
    form_class = ProjectsForm
    template_name = 'project/project_form.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProjectCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.status = PROJECT_STATUS_CHOICES[0][0]
        form.instance.creator = self.request.user
        return super(ProjectCreate, self).form_valid(form)

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Le projet à bien été soumis!'
        )
        return self.object.get_absolute_url()


class SubProjectCreate(generic.CreateView):
    form_class = SubProjectsForm
    template_name = 'project/subproject_form.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SubProjectCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.project = Project.objects.\
            get(id=self.kwargs['projectID'])
        return super(SubProjectCreate, self).form_valid(form)

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Le sous-projet à bien été ajouté!'
        )
        return self.object.get_absolute_url()


class ProjectUpdate(generic.UpdateView):
    # For update a grants
    model = Project
    form_class = ProjectsForm
    template_name = "project/project_form.html"

    # You need to be connected, and you need to have access
    # as founder or Centech
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        project = get_object_or_404(Project, id=self.object.id)
        if project.creator == self.request.user:
            return super(ProjectUpdate, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'projects:project_detail',
            kwargs={'pk': self.object.id}
        )


class SubProjectDelete(generic.DeleteView):
    form_class = SubProjectsForm
    context_object_name = 'subProject'
    template_name = 'project/subproject_delete.html'
    model = SubProject
    pk_url_kwarg = 'subProjectID'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        subproject = get_object_or_404(
            SubProject,
            id=self.kwargs['subProjectID']
        )
        is_creator = self.request.user == subproject.project.creator
        is_staff = self.request.user.is_staff

        if is_staff or is_creator:
            return super(SubProjectDelete, self).dispatch(*args, **kwargs)
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                'Vous ne disposer des droits nécessaire'
                ' afin de supprimer ce sous-projet!'
            )
            return redirect(reverse_lazy(
                "projects:project_list"
            ))

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Le sous-projet à bien été supprimé!'
        )
        return self.object.get_absolute_url()


def accept_project(request, id_of_project):
    project = Project.objects.get(id=id_of_project)
    project.status = PROJECT_STATUS_CHOICES[1][0]
    project.save(update_fields=['status'])

    messages.add_message(
        request,
        messages.SUCCESS,
        'Le projet à bien été accepté!'
    )
    return redirect(reverse_lazy(
        "projects:project_detail",
        args=[project.id]
    ))


def refuse_project(request, id_of_project):
    project = Project.objects.get(id=id_of_project)
    project.status = PROJECT_STATUS_CHOICES[2][0]
    project.save(update_fields=['status'])

    messages.add_message(
        request,
        messages.WARNING,
        'Le projet a été refusé!'
    )
    return redirect(reverse_lazy(
        "projects:project_detail",
        args=[project.id]
    ))
