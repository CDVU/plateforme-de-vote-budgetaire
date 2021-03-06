# coding: utf-8

from django.views import generic
from vote.models import Vote, Poll, Choice
from project.models import SubProject
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.shortcuts import get_object_or_404


class Form(generic.DetailView):
    model = Vote
    template_name = 'vote/form.html'

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        vote = get_object_or_404(
            Vote,
            id=self.kwargs['pk']
        )

        if request.user in vote.users.all():
            messages.add_message(
                request,
                messages.ERROR,
                'Vous avez déjà voté sur cette session de vote.'
            )

            response = reverse('votes:home')
            return HttpResponseRedirect(response)
        else:
            return super(Form, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        vote = Vote.objects.get(id=kwargs['pk'])
        project_list = []

        # We make the list of accepted project
        for project in vote.projects.all():
            if 'project-' + str(project.id) in request.POST:
                project_list.append(project.id)

        # We make the list of subProject accepted in accepted project
        # (idSubProject, minAmount, maxAmount)
        sub_project_list = []
        for project in project_list:
            sub_projects = SubProject.objects.filter(project__id=project)
            for sub_project in sub_projects:
                if 'subProject-' + str(sub_project.id) in request.POST:
                    tuple_sub_project = (
                        sub_project.id,
                        sub_project.minimum_amount,
                        sub_project.maximum_amount
                    )

                    sub_project_list.append(tuple_sub_project)

        # Check if the vote.amount is respected
        amount = 0
        for elem in sub_project_list:
            post_amount = int(
                request.POST['subProject-' + str(elem[0]) + '-amount']
            )
            # Check if each amount is valid
            if elem[1] <= post_amount:
                if elem[2] >= post_amount:
                    amount += int(
                        request.POST['subProject-' + str(elem[0]) + '-amount']
                    )
                else:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        'Une erreur est survenue, si le problème '
                        'persiste veuillez nous contacter !'
                    )
                    response = reverse(
                        'votes:form',
                        kwargs={'pk': vote.id}
                    )
                    return HttpResponseRedirect(response)
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Une erreur est survenue, si le problème '
                    'persiste veuillez nous contacter !'
                )
                response = reverse(
                    'votes:form',
                    kwargs={'pk': vote.id}
                )
                return HttpResponseRedirect(response)

        if amount > vote.amount:
            messages.add_message(
                request,
                messages.ERROR,
                'Une erreur est survenu avec votre budget, celui-ci est '
                'supérieur au budget disponible. Veuillez recommencer!'
            )
            response = reverse(
                'votes:form',
                kwargs={'pk': vote.id}
            )
            return HttpResponseRedirect(response)

        # Create the poll
        poll = Poll.objects.create(vote=vote)

        # Create each choice of the poll
        for elem in sub_project_list:
            amount = request.POST['subProject-' + str(elem[0]) + '-amount']
            sub_project = SubProject.objects.get(id=elem[0])
            Choice.objects.create(
                poll=poll,
                amount=amount,
                sub_project=sub_project
            )

        # Add user in the list of participants
        vote.users.add(request.user)

        messages.add_message(
            request,
            messages.SUCCESS,
            'Votre vote a été pris en compte. Nous vous remercions de '
            'votre participation.'
        )
        response = reverse('votes:home')
        return HttpResponseRedirect(response)


class Home(generic.TemplateView):
    template_name = 'vote/home.html'

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(Home, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)

        list_vote = []

        votes = Vote.objects.filter(
            start_date__lt=datetime.now(),
            end_date__gt=datetime.now()
        ).order_by('-start_date')

        for vote in votes:
            has_voted = self.request.user in vote.users.all()
            list_vote.append((vote, has_voted))

        context['votes'] = list_vote

        return context
