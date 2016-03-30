# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subproject',
            name='project',
            field=models.ForeignKey(related_name='SubProjet', default=None, verbose_name=b'Projet', to='project.Project'),
            preserve_default=False,
        ),
    ]
