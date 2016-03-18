# coding: utf-8

from django.db import models

PROJECT_STATUS_CHOICES = (
    ('In waiting', 0),
    ('Accepted', 1),
    ('Rejected', 2)
)


class Project(models.Model):
    class Meta:
        verbose_name_plural = 'Projets'


    name = models.CharField(
        verbose_name='Nom',
        max_length=100
    )

    description = models.TextField(
        verbose_name='Description'
    )

    number_affected_by = models.PositiveIntegerField(
        verbose_name='Nombre de personne affectées'
    )

    justification = models.TextField(
        verbose_name='Justification'
    )

    completion_time = models.DurationField(
        verbose_name='Temps de réalisation'
    )

    date_of_submission = models.DateTimeField(
        verbose_name='Date de soumission'
    )

    author_name = models.CharField(
        verbose_name='Nom',
        max_length=100
    )

    author_website = models.TextField(
        verbose_name='Site web'
    )

    author_description = models.TextField(
        verbose_name='Description'
    )

    status = models.CharField(
        verbose_name='Validé',
        max_length=100,
        choices=PROJECT_STATUS_CHOICES
    )

    def __str__(self):
        return self.name


class SubProject(models.Model):
    class Meta:
        verbose_name_plural = 'Sous-Projets'


    name = models.CharField(
        verbose_name='Nom',
        max_length=100
    )

    description = models.TextField(
        verbose_name='Description'
    )

    completion_time = models.DurationField(
        verbose_name='Temps de réalisation'
    )

    minimum_amount = models.PositiveIntegerField(
        verbose_name='Montant minimal'
    )

    maximum_amount = models.PositiveIntegerField(
        verbose_name='Montant maximal'
    )

    def __str__(self):
        return self.name
