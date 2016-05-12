# coding: utf-8

import factory
import datetime
from project.models import Project, SubProject, PROJECT_STATUS_CHOICES
from vote.models import Vote


class VoteFactory(factory.DjangoModelFactory):
    class Meta:
        model = Vote

    start_date = datetime.datetime(2016, 4, 1, 14, 41, 39)
    end_date = datetime.datetime(2016, 6, 20, 14, 41, 39)
    amount = 30000
