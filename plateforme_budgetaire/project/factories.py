# coding: utf-8

import factory, datetime
from project.models import Project, SubProject, PROJECT_STATUS_CHOICES


class ProjectFactory(factory.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Sequence('Projet ïtrema755 N°{0}'.format)
    description = "Aliquam et qui et sit voluptas voluptas dolorem." \
                  " Nam ut est et quia est aut minima. Tenetur sunt" \
                  " sed ea et molestias et qui quia. Non distinctio" \
                  " beatae aut sit blanditiis corporis mollitia." \
                  " Tempora dolor assumenda qui dolorem. Error" \
                  " reiciendis corporis est ut atque ex in. Quae" \
                  " voluptate culpa ut in voluptatem voluptas" \
                  " voluptatibus quis. Provident quia fugit est" \
                  " eaque fuga corrupti eaque. Minima quaerat" \
                  " cupiditate nihil quidem. Sit ut nobis velit" \
                  " asperiores voluptas autem quaerat. Sunt esse sunt" \
                  " id natus voluptate facilis a et. Et et est ipsa" \
                  " veritatis consequatur. Id unde nisi aut. Esse" \
                  " dolorem laborum saepe provident voluptas odit" \
                  " debitis."

    number_affected_by = 200
    justification = "Vitae et aspernatur odit repellat atque consequatur" \
                    " harum totam. Quia illo deserunt sed quam quo atque" \
                    " iste non. Quaerat id neque aspernatur quia aut et." \
                    " Sit aut porro exercitationem magnam enim enim culpa." \
                    " Sapiente odit fuga dolorem quo ut laboriosam. Omnis" \
                    " aut voluptatem sint omnis ex quidem. Et minus" \
                    " eligendi asperiores. Ipsam sint voluptatum minima" \
                    " quis vero ut. Sint autem qui dicta excepturi" \
                    " similique voluptatem at. Sint exercitationem" \
                    " numquam esse blanditiis error quae omnis. Optio" \
                    " perspiciatis et neque vel."

    completion_time = datetime.timedelta(1157, 35200)
    date_of_submission = datetime.datetime(2016, 4, 1, 14, 41, 39)
    author_name = "Noël Rignon"
    author_website = "https://RignonNoel.github.io"
    author_description = "Étudiant en génie logiciel, auxiliaire de" \
                         " recherche à Maison du logiciel libre et" \
                         " consultant pour le Centech."

    status = PROJECT_STATUS_CHOICES[0][0]

    @classmethod
    def __init__(self, **kwargs):
        creator = kwargs.pop('creator', None)

        project = super(ProjectFactory, self).__init__(self, **kwargs)
        project.save()


class SubProjectFactory(factory.DjangoModelFactory):
    class Meta:
        model = SubProject

    name = factory.Sequence('Sous-projet ïtrema755 N°{0}'.format)
    description = "Aliquam et qui et sit voluptas voluptas dolorem." \
                  " Nam ut est et quia est aut minima. Tenetur sunt" \
                  " sed ea et molestias et qui quia. Non distinctio" \
                  " beatae aut sit blanditiis corporis mollitia." \
                  " Tempora dolor assumenda qui dolorem. Error" \
                  " reiciendis corporis est ut atque ex in. Quae" \
                  " voluptate culpa ut in voluptatem voluptas" \
                  " voluptatibus quis. Provident quia fugit est" \
                  " eaque fuga corrupti eaque. Minima quaerat" \
                  " cupiditate nihil quidem. Sit ut nobis velit" \
                  " asperiores voluptas autem quaerat. Sunt esse sunt" \
                  " id natus voluptate facilis a et. Et et est ipsa" \
                  " veritatis consequatur. Id unde nisi aut. Esse" \
                  " dolorem laborum saepe provident voluptas odit" \
                  " debitis."

    completion_time = datetime.timedelta(1157, 35200)
    minimum_amount = 1000
    maximum_amount = 3000

    @classmethod
    def __init__(self, **kwargs):
        project = kwargs.pop('project', None)

        sub_project = super(SubProjectFactory, self).__init__(self, **kwargs)
        sub_project.save()
