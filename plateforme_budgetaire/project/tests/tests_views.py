# coding: utf-8

from django.test import TestCase
from project.factories import ProjectFactory, SubProjectFactory
from vote.factories import VoteFactory
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
import datetime
from project.models import Project, PROJECT_STATUS_CHOICES, SubProject


class ProjectListViewTests(TestCase):

    def setUp(self):
        settings.EMAIL_BACKEND = \
            'django.core.mail.backends.locmem.EmailBackend'

        self.user = User.objects.create_user(
            username='am56680@ens.etsmtl.ca',
            email='am56680@ens.etsmtl.ca',
            password='passUser'
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            email='rignon.noel@openmailbox.org',
            password='passAdmin'
        )
        self.project = ProjectFactory(creator=self.user)
        self.sub_project_1 = SubProjectFactory(project=self.project)
        self.sub_project_2 = SubProjectFactory(project=self.project)

        self.project_2 = ProjectFactory(creator=self.admin)
        self.sub_project_3 = SubProjectFactory(project=self.project_2)
        self.sub_project_4 = SubProjectFactory(project=self.project_2)

    def test_access_as_user(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.get(
            reverse('projects:project_list'),
            follow=False
        )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(1, len(result.context['projects']))

    def test_access_as_admin(self):
        self.client.logout()
        self.client.login(
            username=self.admin.username,
            password="passAdmin"
        )

        result = self.client.get(
            reverse('projects:project_list'),
            follow=False
        )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(2, len(result.context['projects']))

    def test_access_as_logout(self):
        self.client.logout()

        result = self.client.get(
            reverse('projects:project_list'),
            follow=False
        )
        self.assertEqual(result.status_code, 302)

    def test_access_with_status_as_user(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.get(
            reverse(
                'projects:project_list',
                kwargs={'validated': 1}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 200)

    def test_access_with_status_as_admin(self):
        self.client.logout()
        self.client.login(
            username=self.admin.username,
            password="passAdmin"
        )

        result = self.client.get(
            reverse(
                'projects:project_list',
                kwargs={'validated': 1}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 200)


class ProjectDetailViewTests(TestCase):

    def setUp(self):
        settings.EMAIL_BACKEND = \
            'django.core.mail.backends.locmem.EmailBackend'

        self.user = User.objects.create_user(
            username='am56680@ens.etsmtl.ca',
            email='am56680@ens.etsmtl.ca',
            password='passUser'
        )
        self.user_2 = User.objects.create_user(
            username='ak12345@ens.etsmtl.ca',
            email='ak12345@ens.etsmtl.ca',
            password='passUser'
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            email='rignon.noel@openmailbox.org',
            password='passAdmin'
        )
        self.project = ProjectFactory(creator=self.user)
        self.sub_project_1 = SubProjectFactory(project=self.project)
        self.sub_project_2 = SubProjectFactory(project=self.project)

        self.project_2 = ProjectFactory(creator=self.user_2)
        self.sub_project_1 = SubProjectFactory(project=self.project_2)
        self.sub_project_2 = SubProjectFactory(project=self.project_2)

    def test_access_as_user(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.get(
            reverse(
                'projects:project_detail',
                kwargs={'pk': self.project.id}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 200)

    def test_access_on_project_inexistant(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.get(
            reverse('projects:project_detail', kwargs={'pk': 99999}),
            follow=False
        )

        self.assertEqual(result.status_code, 404)

    def test_user_not_owner_on_project(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.get(
            reverse(
                'projects:project_detail',
                kwargs={'pk': self.project_2.id}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 302)

    def test_access_as_admin(self):
        self.client.logout()
        self.client.login(
            username=self.admin.username,
            password="passAdmin"
        )

        result = self.client.get(
            reverse(
                'projects:project_detail',
                kwargs={'pk': self.project.id}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 200)

    def test_access_as_logout(self):
        self.client.logout()

        result = self.client.get(
            reverse(
                'projects:project_detail',
                kwargs={'pk': self.project.id}
            ),
            follow=False
        )
        self.assertEqual(result.status_code, 302)


class ProjectCreateViewTests(TestCase):

    def setUp(self):
        settings.EMAIL_BACKEND = \
            'django.core.mail.backends.locmem.EmailBackend'

        self.user = User.objects.create_user(
            username='am56680@ens.etsmtl.ca',
            email='am56680@ens.etsmtl.ca',
            password='passUser'
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            email='rignon.noel@openmailbox.org',
            password='passAdmin'
        )

    def test_access_as_user(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.get(
            reverse('projects:project_create'),
            follow=False
        )

        self.assertEqual(result.status_code, 200)

    def test_access_as_admin(self):
        self.client.logout()
        self.client.login(
            username=self.admin.username,
            password="passAdmin"
        )

        result = self.client.get(
            reverse('projects:project_create'),
            follow=False
        )

        self.assertEqual(result.status_code, 200)

    def test_access_as_logout(self):
        self.client.logout()

        result = self.client.get(
            reverse('projects:project_create'),
            follow=False
        )
        self.assertEqual(result.status_code, 302)

    def test_add_a_project(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        data = {
            'name': 'Nouveau projet',
            'description': 'Ma description',
            'number_affected_by': '345',
            'justification': 'Ma justification',
            'completion_time': datetime.timedelta(1157, 35200),
            'date_of_submission': datetime.datetime(2016, 4, 1, 14, 41, 39),
            'author_name': 'Noël Rignon',
            'author_website': 'http://RignonNoel.github.io',
            'author_description': 'Étudiant génie logiciel',
        }

        result = self.client.post(
            reverse('projects:project_create'),
            data,
            follow=False
        )
        self.assertEqual(result.status_code, 302)

    def test_missing_fields_when_add_a_project(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        data = {
            'name': 'Nouveau projet'
        }

        result = self.client.post(
            reverse('projects:project_create'),
            data,
            follow=False
        )
        self.assertEqual(result.status_code, 200)


class SubProjectCreateViewTests(TestCase):

    def setUp(self):
        settings.EMAIL_BACKEND = \
            'django.core.mail.backends.locmem.EmailBackend'

        self.user = User.objects.create_user(
            username='am56680@ens.etsmtl.ca',
            email='am56680@ens.etsmtl.ca',
            password='passUser'
        )
        self.user_2 = User.objects.create_user(
            username='ak12345@ens.etsmtl.ca',
            email='ak12345@ens.etsmtl.ca',
            password='passUser'
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            email='rignon.noel@openmailbox.org',
            password='passAdmin'
        )

        self.project = ProjectFactory(creator=self.user)
        self.sub_project_1 = SubProjectFactory(project=self.project)
        self.sub_project_2 = SubProjectFactory(project=self.project)

        self.project_2 = ProjectFactory(creator=self.user_2)
        self.sub_project_3 = SubProjectFactory(project=self.project_2)
        self.sub_project_4 = SubProjectFactory(project=self.project_2)

    def test_access_as_user(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.get(
            reverse(
                'projects:subproject_create',
                kwargs={'projectID': self.project.id}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 200)

    def test_access_as_admin(self):
        self.client.logout()
        self.client.login(
            username=self.admin.username,
            password="passAdmin"
        )

        result = self.client.get(
            reverse(
                'projects:subproject_create',
                kwargs={'projectID': self.project.id}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 200)

    def test_user_not_owner_on_project(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.get(
            reverse(
                'projects:project_update',
                kwargs={'pk': self.project_2.id}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 302)

    def test_access_as_logout(self):
        self.client.logout()

        result = self.client.get(
            reverse(
                'projects:subproject_create',
                kwargs={'projectID': self.project.id}
            ),
            follow=False
        )
        self.assertEqual(result.status_code, 302)

    def test_add_a_subproject(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        data = {
            'name': 'Nouveau projet',
            'description': 'Ma description',
            'completion_time': datetime.timedelta(1157, 35200),
            'minimum_amount': 1000,
            'maximum_amount': 2000,
        }

        result = self.client.post(
            reverse(
                'projects:subproject_create',
                kwargs={'projectID': self.project.id}
            ),
            data,
            follow=False
        )
        self.assertEqual(result.status_code, 302)

    def test_error_on_amount(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        data = {
            'name': 'Nouveau projet',
            'description': 'Ma description',
            'completion_time': datetime.timedelta(1157, 35200),
            'minimum_amount': 3000,
            'maximum_amount': 2000,
        }

        result = self.client.post(
            reverse(
                'projects:subproject_create',
                kwargs={'projectID': self.project.id}
            ),
            data,
            follow=False
        )
        self.assertEqual(result.status_code, 200)
        self.assertContains(result, "Le montant maximal doit être supérieur"
                                    " au montant minimal.")

    def test_missing_fields_when_add_a_subproject(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        data = {
            'name': 'Nouveau sous-projet'
        }

        result = self.client.post(
            reverse(
                'projects:subproject_create',
                kwargs={'projectID': self.project.id}
            ),
            data,
            follow=False
        )
        self.assertEqual(result.status_code, 200)


class ProjectUpdateViewTests(TestCase):

    def setUp(self):
        settings.EMAIL_BACKEND = \
            'django.core.mail.backends.locmem.EmailBackend'

        self.user = User.objects.create_user(
            username='am56680@ens.etsmtl.ca',
            email='am56680@ens.etsmtl.ca',
            password='passUser'
        )
        self.user_2 = User.objects.create_user(
            username='ak12345@ens.etsmtl.ca',
            email='ak12345@ens.etsmtl.ca',
            password='passUser'
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            email='rignon.noel@openmailbox.org',
            password='passAdmin'
        )

        self.project = ProjectFactory(creator=self.user)
        self.sub_project_1 = SubProjectFactory(project=self.project)
        self.sub_project_2 = SubProjectFactory(project=self.project)

        self.project_2 = ProjectFactory(creator=self.user_2)
        self.sub_project_3 = SubProjectFactory(project=self.project_2)
        self.sub_project_4 = SubProjectFactory(project=self.project_2)

    def test_access_as_user(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.get(
            reverse(
                'projects:project_update',
                kwargs={'pk': self.project.id}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 200)

    def test_access_as_admin(self):
        self.client.logout()
        self.client.login(
            username=self.admin.username,
            password="passAdmin"
        )

        result = self.client.get(
            reverse(
                'projects:project_update',
                kwargs={'pk': self.project.id}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 200)

    def test_user_not_owner_on_project(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.get(
            reverse(
                'projects:project_update',
                kwargs={'pk': self.project_2.id}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 302)

    def test_access_as_logout(self):
        self.client.logout()

        result = self.client.get(
            reverse(
                'projects:project_update',
                kwargs={'pk': self.project.id}
            ),
            follow=False
        )
        self.assertEqual(result.status_code, 302)

    def test_update_a_project(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        data = {
            'name': 'Ancien projet',
            'description': 'Ancienne description',
            'number_affected_by': '359',
            'justification': 'Ancienne justification',
            'completion_time': datetime.timedelta(1157, 35400),
            'date_of_submission': datetime.datetime(2016, 5, 8, 14, 41, 39),
            'author_name': 'Rignon Noël',
            'author_website': 'http://duckduckgo.com',
            'author_description': 'Étudiant en génie',
        }

        result = self.client.post(
            reverse(
                'projects:project_update',
                kwargs={'pk': self.project.id}
            ),
            data,
            follow=False
        )
        self.assertEqual(result.status_code, 302)

    def test_update_just_one_field_of_project(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        data = {
            'name': 'Nouveau sous-projet'
        }

        result = self.client.post(
            reverse(
                'projects:project_update',
                kwargs={'pk': self.project.id}
            ),
            data,
            follow=False
        )
        self.assertEqual(result.status_code, 200)

    def test_update_no_field_of_project(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        data = {}

        result = self.client.post(
            reverse(
                'projects:project_update',
                kwargs={'pk': self.project.id}
            ),
            data,
            follow=False
        )
        self.assertEqual(result.status_code, 200)


class SubProjectUpdateViewTests(TestCase):

    def setUp(self):
        settings.EMAIL_BACKEND = \
            'django.core.mail.backends.locmem.EmailBackend'

        self.user = User.objects.create_user(
            username='am56680@ens.etsmtl.ca',
            email='am56680@ens.etsmtl.ca',
            password='passUser'
        )
        self.user_2 = User.objects.create_user(
            username='ak12345@ens.etsmtl.ca',
            email='ak12345@ens.etsmtl.ca',
            password='passUser'
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            email='rignon.noel@openmailbox.org',
            password='passAdmin'
        )

        self.project = ProjectFactory(creator=self.user)
        self.sub_project_1 = SubProjectFactory(project=self.project)
        self.sub_project_2 = SubProjectFactory(project=self.project)

        self.project_2 = ProjectFactory(creator=self.user_2)
        self.sub_project_3 = SubProjectFactory(project=self.project_2)
        self.sub_project_4 = SubProjectFactory(project=self.project_2)

    def test_access_as_user(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.get(
            reverse(
                'projects:subproject_update',
                kwargs={'pk': self.sub_project_1.id}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 200)

    def test_access_as_admin(self):
        self.client.logout()
        self.client.login(
            username=self.admin.username,
            password="passAdmin"
        )

        result = self.client.get(
            reverse(
                'projects:project_update',
                kwargs={'pk': self.sub_project_1.id}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 200)

    def test_user_not_owner_on_project(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.get(
            reverse(
                'projects:subproject_update',
                kwargs={'pk': self.sub_project_3.id}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 302)

    def test_access_as_logout(self):
        self.client.logout()

        result = self.client.get(
            reverse(
                'projects:subproject_update',
                kwargs={'pk': self.sub_project_1.id}
            ),
            follow=False
        )
        self.assertEqual(result.status_code, 302)

    def test_update_a_subproject(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        data = {
            'name': 'Nouveau nom pour sous-projet',
            'description': 'Ma nouvelle description du sous projet',
            'completion_time': '1 Mois',
            'minimum_amount': 2000,
            'maximum_amount': 3000,
        }

        result = self.client.post(
            reverse(
                'projects:subproject_update',
                kwargs={'pk': self.sub_project_1.id}
            ),
            data,
            follow=False
        )
        self.assertEqual(result.status_code, 302)

    def test_update_just_one_field_of_subproject(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        data = {
            'name': 'Nouveau nom pour sous-projet'
        }

        result = self.client.post(
            reverse(
                'projects:subproject_update',
                kwargs={'pk': self.sub_project_1.id}
            ),
            data,
            follow=False
        )
        self.assertEqual(result.status_code, 200)

    def test_update_no_field_of_subproject(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        data = {}

        result = self.client.post(
            reverse(
                'projects:subproject_update',
                kwargs={'pk': self.sub_project_1.id}
            ),
            data,
            follow=False
        )
        self.assertEqual(result.status_code, 200)


class ProjectDeleteViewTests(TestCase):

    def setUp(self):
        settings.EMAIL_BACKEND = \
            'django.core.mail.backends.locmem.EmailBackend'

        self.user = User.objects.create_user(
            username='am56680@ens.etsmtl.ca',
            email='am56680@ens.etsmtl.ca',
            password='passUser'
        )
        self.user_2 = User.objects.create_user(
            username='ak12345@ens.etsmtl.ca',
            email='ak12345@ens.etsmtl.ca',
            password='passUser'
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            email='rignon.noel@openmailbox.org',
            password='passAdmin'
        )

        self.project = ProjectFactory(creator=self.user)
        self.sub_project_1 = SubProjectFactory(project=self.project)
        self.sub_project_2 = SubProjectFactory(project=self.project)

        self.project_2 = ProjectFactory(creator=self.user_2)
        self.sub_project_3 = SubProjectFactory(project=self.project_2)
        self.sub_project_4 = SubProjectFactory(project=self.project_2)

    def test_access_as_user(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.get(
            reverse(
                'projects:project_delete',
                kwargs={'pk': self.project.id}
            ),
            follow=False
        )
        self.assertEqual(result.status_code, 200)

    def test_delete_as_user(self):
        project_to_delete = ProjectFactory(creator=self.user)
        id_of_project = project_to_delete.id

        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.post(
            reverse(
                'projects:project_delete',
                kwargs={'pk': id_of_project}
            ),
            follow=True
        )

        self.assertEqual(0, Project.objects.filter(id=id_of_project).count())
        self.assertContains(result, "Le projet à bien été supprimé!")
        self.assertRedirects(
            result,
            reverse('projects:project_list'),
            status_code=302
        )

    def test_delete_as_user_project_in_vote(self):
        project_to_delete = ProjectFactory(creator=self.user)
        id_of_project = project_to_delete.id

        vote = VoteFactory()
        vote.projects.add(project_to_delete)

        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.post(
            reverse(
                'projects:project_delete',
                kwargs={'pk': id_of_project}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 302)

    def test_access_as_admin(self):
        self.client.logout()
        self.client.login(
            username=self.admin.username,
            password="passAdmin"
        )

        result = self.client.get(
            reverse(
                'projects:project_delete',
                kwargs={'pk': self.project.id}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 200)

    def test_delete_as_admin(self):
        project_to_delete = ProjectFactory(creator=self.user)
        id_of_project = project_to_delete.id

        self.client.logout()
        self.client.login(
            username=self.admin.username,
            password="passAdmin"
        )

        result = self.client.post(
            reverse(
                'projects:project_delete',
                kwargs={'pk': id_of_project}
            ),
            follow=True
        )

        self.assertEqual(0, Project.objects.filter(id=id_of_project).count())
        self.assertContains(result, "Le projet à bien été supprimé!")
        self.assertRedirects(
            result,
            reverse('projects:project_list'),
            status_code=302
        )

    def test_delete_as_admin_project_in_vote(self):
        project_to_delete = ProjectFactory(creator=self.user)
        id_of_project = project_to_delete.id

        vote = VoteFactory()
        vote.projects.add(project_to_delete)

        self.client.logout()
        self.client.login(
            username=self.admin.username,
            password="passAdmin"
        )

        result = self.client.post(
            reverse(
                'projects:project_delete',
                kwargs={'pk': id_of_project}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 302)

    def test_user_not_owner_on_project(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.get(
            reverse(
                'projects:project_delete',
                kwargs={'pk': self.project_2.id}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 302)

    def test_delete_as_user_not_owner_on_project(self):
        project_to_delete = ProjectFactory(creator=self.user)
        id_of_project = project_to_delete.id

        self.client.logout()
        self.client.login(
            username=self.user_2.username,
            password="passUser"
        )

        result = self.client.post(
            reverse(
                'projects:project_delete',
                kwargs={'pk': id_of_project}
            ),
            follow=True
        )

        self.assertEqual(1, Project.objects.filter(id=id_of_project).count())
        self.assertContains(
            result,
            "Vous ne disposer des droits nécessaire "
            "afin de supprimer ce projet!"
        )
        self.assertRedirects(
            result,
            reverse('projects:project_list'),
            status_code=302
        )

    def test_delete_as_user_not_owner_on_project_in_vote(self):
        project_to_delete = ProjectFactory(creator=self.user)
        id_of_project = project_to_delete.id

        vote = VoteFactory()
        vote.projects.add(project_to_delete)

        self.client.logout()
        self.client.login(
            username=self.user_2.username,
            password="passUser"
        )

        result = self.client.post(
            reverse(
                'projects:project_delete',
                kwargs={'pk': id_of_project}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 302)

    def test_access_as_logout(self):
        self.client.logout()

        result = self.client.get(
            reverse(
                'projects:project_delete',
                kwargs={'pk': self.project.id}
            ),
            follow=False
        )
        self.assertEqual(result.status_code, 302)

    def test_delete_as_logout(self):
        project_to_delete = ProjectFactory(creator=self.user)
        id_of_project = project_to_delete.id

        self.client.logout()

        result = self.client.post(
            reverse(
                'projects:project_delete',
                kwargs={'pk': id_of_project}
            ),
            follow=False
        )

        self.assertEqual(1, Project.objects.filter(id=id_of_project).count())
        self.assertEqual(result.status_code, 302)

    def test_delete_as_logout_project_in_vote(self):
        project_to_delete = ProjectFactory(creator=self.user)
        id_of_project = project_to_delete.id

        vote = VoteFactory()
        vote.projects.add(project_to_delete)

        self.client.logout()

        result = self.client.post(
            reverse(
                'projects:project_delete',
                kwargs={'pk': id_of_project}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 302)


class SubProjectDeleteViewTests(TestCase):

    def setUp(self):
        settings.EMAIL_BACKEND = \
            'django.core.mail.backends.locmem.EmailBackend'

        self.user = User.objects.create_user(
            username='am56680@ens.etsmtl.ca',
            email='am56680@ens.etsmtl.ca',
            password='passUser'
        )
        self.user_2 = User.objects.create_user(
            username='ak12345@ens.etsmtl.ca',
            email='ak12345@ens.etsmtl.ca',
            password='passUser'
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            email='rignon.noel@openmailbox.org',
            password='passAdmin'
        )

        self.project = ProjectFactory(creator=self.user)
        self.sub_project_1 = SubProjectFactory(project=self.project)
        self.sub_project_2 = SubProjectFactory(project=self.project)

        self.project_2 = ProjectFactory(creator=self.user_2)
        self.sub_project_3 = SubProjectFactory(project=self.project_2)
        self.sub_project_4 = SubProjectFactory(project=self.project_2)

    def test_access_as_user(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.get(
            reverse(
                'projects:subproject_delete',
                kwargs={'subProjectID': self.sub_project_1.id}
            ),
            follow=False
        )
        self.assertEqual(result.status_code, 200)

    def test_delete_as_user(self):
        id_of_subproject = self.sub_project_1.id
        id_of_project = self.sub_project_1.project.id

        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.post(
            reverse(
                'projects:subproject_delete',
                kwargs={'subProjectID': id_of_subproject}
            ),
            follow=True
        )

        self.assertEqual(
            0,
            SubProject.objects.filter(id=id_of_subproject).count()
        )
        self.assertRedirects(
            result,
            reverse(
                'projects:project_detail',
                kwargs={'pk': id_of_project}
            ),
            status_code=302
        )

    def test_delete_as_user_project_in_vote(self):
        id_of_subproject = self.sub_project_1.id
        id_of_project = self.sub_project_1.project.id

        vote = VoteFactory()
        vote.projects.add(self.sub_project_1.project)

        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.post(
            reverse(
                'projects:subproject_delete',
                kwargs={'subProjectID': id_of_subproject}
            ),
            follow=True
        )

        self.assertEqual(
            1,
            SubProject.objects.filter(id=id_of_subproject).count()
        )
        self.assertRedirects(
            result,
            reverse(
                'projects:project_detail',
                kwargs={'pk': id_of_project}
            ),
            status_code=302
        )

    def test_access_as_admin(self):
        self.client.logout()
        self.client.login(
            username=self.admin.username,
            password="passAdmin"
        )

        result = self.client.get(
            reverse(
                'projects:subproject_delete',
                kwargs={'subProjectID': self.sub_project_1.id}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 200)

    def test_delete_as_admin(self):
        id_of_subproject = self.sub_project_1.id
        id_of_project = self.sub_project_1.project.id

        self.client.logout()
        self.client.login(
            username=self.admin.username,
            password="passAdmin"
        )

        result = self.client.post(
            reverse(
                'projects:subproject_delete',
                kwargs={'subProjectID': self.sub_project_1.id}
            ),
            follow=True
        )

        self.assertEqual(
            0,
            SubProject.objects.filter(id=id_of_subproject).count()
        )
        self.assertRedirects(
            result,
            reverse(
                'projects:project_detail',
                kwargs={'pk': id_of_project}
            ),
            status_code=302
        )

    def test_delete_as_admin_project_in_vote(self):
        id_of_subproject = self.sub_project_1.id
        id_of_project = self.sub_project_1.project.id

        vote = VoteFactory()
        vote.projects.add(self.sub_project_1.project)

        self.client.logout()
        self.client.login(
            username=self.admin.username,
            password="passAdmin"
        )

        result = self.client.post(
            reverse(
                'projects:subproject_delete',
                kwargs={'subProjectID': id_of_subproject}
            ),
            follow=True
        )

        self.assertEqual(
            1,
            SubProject.objects.filter(id=id_of_subproject).count()
        )
        self.assertRedirects(
            result,
            reverse(
                'projects:project_detail',
                kwargs={'pk': id_of_project}
            ),
            status_code=302
        )

    def test_user_not_owner_on_project(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.get(
            reverse(
                'projects:subproject_delete',
                kwargs={'subProjectID': self.sub_project_3.id}
            ),
            follow=True
        )

        self.assertRedirects(
            result,
            reverse(
                'projects:project_list',
            ),
            status_code=302
        )

    def test_delete_as_user_not_owner_on_project(self):
        id_of_subproject = self.sub_project_1.id

        self.client.logout()
        self.client.login(
            username=self.user_2.username,
            password="passUser"
        )

        result = self.client.post(
            reverse(
                'projects:subproject_delete',
                kwargs={'subProjectID': id_of_subproject}
            ),
            follow=True
        )

        self.assertEqual(
            1,
            SubProject.objects.filter(id=id_of_subproject).count()
        )
        self.assertRedirects(
            result,
            reverse('projects:project_list'),
            status_code=302
        )

    def test_delete_as_user_not_owner_on_project_in_vote(self):
        id_of_subproject = self.sub_project_1.id

        vote = VoteFactory()
        vote.projects.add(self.sub_project_1.project)

        self.client.logout()
        self.client.login(
            username=self.user_2.username,
            password="passUser"
        )

        result = self.client.post(
            reverse(
                'projects:subproject_delete',
                kwargs={'subProjectID': id_of_subproject}
            ),
            follow=True
        )

        self.assertEqual(
            1,
            SubProject.objects.filter(id=id_of_subproject).count()
        )
        self.assertRedirects(
            result,
            reverse('projects:project_list'),
            status_code=302
        )

    def test_access_as_logout(self):
        self.client.logout()

        result = self.client.get(
            reverse(
                'projects:subproject_delete',
                kwargs={'subProjectID': self.sub_project_1.id}
            ),
            follow=False
        )
        self.assertEqual(result.status_code, 302)

    def test_delete_as_logout(self):
        id_of_subproject = self.sub_project_1.id

        self.client.logout()

        result = self.client.post(
            reverse(
                'projects:subproject_delete',
                kwargs={'subProjectID': id_of_subproject}
            ),
            follow=False
        )

        self.assertEqual(
            1,
            SubProject.objects.filter(id=id_of_subproject).count()
        )
        self.assertEqual(result.status_code, 302)

    def test_delete_as_logout_project_in_vote(self):
        id_of_subproject = self.sub_project_1.id

        vote = VoteFactory()
        vote.projects.add(self.sub_project_1.project)

        self.client.logout()

        result = self.client.post(
            reverse(
                'projects:subproject_delete',
                kwargs={'subProjectID': id_of_subproject}
            ),
            follow=False
        )

        self.assertEqual(result.status_code, 302)


class AcceptProjectViewTests(TestCase):

    def setUp(self):
        settings.EMAIL_BACKEND = \
            'django.core.mail.backends.locmem.EmailBackend'

        self.user = User.objects.create_user(
            username='am56680@ens.etsmtl.ca',
            email='am56680@ens.etsmtl.ca',
            password='passUser'
        )
        self.user_2 = User.objects.create_user(
            username='ak12345@ens.etsmtl.ca',
            email='ak12345@ens.etsmtl.ca',
            password='passUser'
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            email='rignon.noel@openmailbox.org',
            password='passAdmin'
        )
        self.project = ProjectFactory(creator=self.user)
        self.sub_project_1 = SubProjectFactory(project=self.project)
        self.sub_project_2 = SubProjectFactory(project=self.project)

        self.project_2 = ProjectFactory(creator=self.user_2)
        self.sub_project_1 = SubProjectFactory(project=self.project_2)
        self.sub_project_2 = SubProjectFactory(project=self.project_2)

    def test_access_as_user(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.get(
            reverse(
                'projects:project_accept',
                kwargs={'pk': self.project.id}
            ),
            follow=True
        )

        # Status of project is the same
        self.assertEqual(
            PROJECT_STATUS_CHOICES[0][0],
            self.project.status
        )

        # Redirection on the good project
        self.assertRedirects(
            result,
            reverse(
                'projects:project_detail',
                kwargs={'pk': self.project.id}
            ),
            status_code=302
        )

    def test_access_on_project_inexistant(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.get(
            reverse('projects:project_accept', kwargs={'pk': 99999}),
            follow=False
        )

        self.assertEqual(result.status_code, 404)

    def test_access_as_admin(self):
        self.client.logout()
        self.client.login(
            username=self.admin.username,
            password="passAdmin"
        )

        result = self.client.get(
            reverse(
                'projects:project_accept',
                kwargs={'pk': self.project.id}
            ),
            follow=True
        )

        project_tested = Project.objects.get(id=self.project.id)

        # Status of project has change
        self.assertEqual(
            PROJECT_STATUS_CHOICES[1][0],
            project_tested.status
        )

        # Validation message is display
        self.assertContains(
            result,
            "Le projet à bien été accepté!"
        )

        # Redirection on the good project
        self.assertRedirects(
            result,
            reverse(
                'projects:project_detail',
                kwargs={'pk': self.project.id}
            ),
            status_code=302
        )

    def test_access_as_logout(self):
        self.client.logout()

        result = self.client.get(
            reverse(
                'projects:project_accept',
                kwargs={'pk': self.project.id}
            ),
            follow=False
        )

        # Status of project no change
        self.assertEqual(
            PROJECT_STATUS_CHOICES[0][0],
            self.project.status
        )

        # Redirection on login page
        self.assertEqual(result.status_code, 302)


class RefuseProjectViewTests(TestCase):

    def setUp(self):
        settings.EMAIL_BACKEND = \
            'django.core.mail.backends.locmem.EmailBackend'

        self.user = User.objects.create_user(
            username='am56680@ens.etsmtl.ca',
            email='am56680@ens.etsmtl.ca',
            password='passUser'
        )
        self.user_2 = User.objects.create_user(
            username='ak12345@ens.etsmtl.ca',
            email='ak12345@ens.etsmtl.ca',
            password='passUser'
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            email='rignon.noel@openmailbox.org',
            password='passAdmin'
        )
        self.project = ProjectFactory(creator=self.user)
        self.sub_project_1 = SubProjectFactory(project=self.project)
        self.sub_project_2 = SubProjectFactory(project=self.project)

        self.project_2 = ProjectFactory(creator=self.user_2)
        self.sub_project_1 = SubProjectFactory(project=self.project_2)
        self.sub_project_2 = SubProjectFactory(project=self.project_2)

    def test_access_as_user(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.get(
            reverse(
                'projects:project_refuse',
                kwargs={'pk': self.project.id}
            ),
            follow=True
        )

        # Status of project is the same
        self.assertEqual(
            PROJECT_STATUS_CHOICES[0][0],
            self.project.status
        )

        # Redirection on the good project
        self.assertRedirects(
            result,
            reverse(
                'projects:project_detail',
                kwargs={'pk': self.project.id}
            ),
            status_code=302
        )

    def test_access_on_project_inexistant(self):
        self.client.logout()
        self.client.login(
            username=self.user.username,
            password="passUser"
        )

        result = self.client.get(
            reverse('projects:project_refuse', kwargs={'pk': 99999}),
            follow=False
        )

        self.assertEqual(result.status_code, 404)

    def test_access_as_admin(self):
        self.client.logout()
        self.client.login(
            username=self.admin.username,
            password="passAdmin"
        )

        result = self.client.get(
            reverse(
                'projects:project_refuse',
                kwargs={'pk': self.project.id}
            ),
            follow=True
        )

        project_tested = Project.objects.get(id=self.project.id)

        # Status of project has change
        self.assertEqual(
            PROJECT_STATUS_CHOICES[2][0],
            project_tested.status
        )

        # Validation message is display
        self.assertContains(
            result,
            "Le projet a été refusé!"
        )

        # Redirection on the good project
        self.assertRedirects(
            result,
            reverse(
                'projects:project_detail',
                kwargs={'pk': self.project.id}
            ),
            status_code=302
        )

    def test_access_as_logout(self):
        self.client.logout()

        result = self.client.get(
            reverse(
                'projects:project_refuse',
                kwargs={'pk': self.project.id}
            ),
            follow=False
        )

        # Status of project no change
        self.assertEqual(
            PROJECT_STATUS_CHOICES[0][0],
            self.project.status
        )

        # Redirection on login page
        self.assertEqual(result.status_code, 302)
