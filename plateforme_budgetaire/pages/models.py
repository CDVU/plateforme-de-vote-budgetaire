# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Hash(models.Model):
    class Meta:
        verbose_name_plural = 'Hashs'


    user = models.ForeignKey(
        User,
        verbose_name='User',
        related_name='Hashs'
    )

    hash = models.TextField(
        verbose_name='hash'
    )

    duration = models.DurationField(
        verbose_name='Temps de vie'
    )

    action = models.TextField(
        verbose_name='Action authorisé'
    )

    created = models.DateTimeField(
        verbose_name='Date of creation'
    )

    used = models.BooleanField(
        verbose_name='Utilisé',
        default=False
    )

    def __str__(self):
        return str(self.user) + ' - ' + str(self.action) + ' - ' + str(self.created)

    def save(self, *args, **kwarg):
        if not self.id:
            self.created = timezone.now()

        super(Hash, self).save(*args, **kwarg)