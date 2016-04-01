# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_subproject_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(max_length=100, verbose_name=b'Valid\xc3\xa9', choices=[(b'En attente', 0), (b'Accept\xc3\xa9', 1), (b'Rejet\xc3\xa9', 2)]),
        ),
        migrations.AlterField(
            model_name='subproject',
            name='project',
            field=models.ForeignKey(related_name='SubProject', verbose_name=b'Projet', to='project.Project'),
        ),
    ]
