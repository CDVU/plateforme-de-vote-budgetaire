# coding: utf-8

from django.test import TestCase
from project.factories import ProjectFactory, SubProjectFactory
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse


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

        # list of projects.
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

        # list of companies.
        result = self.client.get(
            reverse(
                'projects:project_detail',
                kwargs={'pk': self.project.id}
            ),
            follow=False
        )
        self.assertEqual(result.status_code, 302)
