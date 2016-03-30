# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20160330_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='author_description',
            field=models.TextField(verbose_name=b"\xc3\x80 propos de l'auteur", blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='author_name',
            field=models.CharField(max_length=100, verbose_name=b"Nom de l'auteur"),
        ),
        migrations.AlterField(
            model_name='project',
            name='author_website',
            field=models.TextField(verbose_name=b"Site web de l'auteur", blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(verbose_name=b'Description du projet'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=100, verbose_name=b'Nom du projet'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(max_length=100, verbose_name=b'Valid\xc3\xa9', choices=[('En attente', 0), ('Accept\xe9', 1), ('Rejet\xe9', 2)]),
        ),
    ]
