# coding: utf-8

from django.db import models
from project.models import Project, SubProject
from django.contrib.auth.models import User
from django.utils import timezone


class Vote(models.Model):
    class Meta:
        verbose_name_plural = 'Votes'

    start_date = models.DateTimeField(
        verbose_name="Date d'ouverture",
    )

    end_date = models.DateTimeField(
        verbose_name='Date de fermeture',
    )

    amount = models.PositiveIntegerField(
        verbose_name="Budget"
    )

    users = models.ManyToManyField(
        User,
        verbose_name='Users',
        related_name='Votes',
        null=True,
        blank=True
    )

    projects = models.ManyToManyField(
        Project,
        verbose_name='Projects',
        related_name='Votes'
    )

    def __unicode__(self):
        return str(self.start_date)


class Poll(models.Model):
    class Meta:
        verbose_name_plural = 'Voix'

    vote = models.ForeignKey(
        Vote,
        verbose_name='Vote',
        related_name='Voix'
    )

    date_of_submission = models.DateTimeField(
        verbose_name='Date de soumission',
    )

    def __unicode__(self):
        return str(self.vote.start_date) + " - " + str(self.date_of_submission)

    def save(self, *args, **kwarg):
        if not self.id:
            self.date_of_submission = timezone.now()

        super(Poll, self).save(*args, **kwarg)


class Choice(models.Model):
    class Meta:
        verbose_name_plural = 'Choix'

    poll = models.ForeignKey(
        Poll,
        verbose_name='Voix',
        related_name='Choix'
    )

    amount = models.PositiveIntegerField(
        verbose_name="Montant"
    )

    sub_project = models.ForeignKey(
        SubProject,
        verbose_name='Sous-projet',
        related_name='Choix'
    )

    def __unicode__(self):
        return str(self.poll.id) + " - " + self.sub_project.name
