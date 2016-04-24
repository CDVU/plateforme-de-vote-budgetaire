# coding: utf-8

from django.test import TestCase
from project.factories import ProjectFactory, SubProjectFactory
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
import datetime


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
