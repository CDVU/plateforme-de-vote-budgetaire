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
