# coding: utf-8

from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
from pages.models import Hash
import datetime


class HomeViewTests(TestCase):

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
            reverse('pages:home'),
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
            reverse('pages:home'),
            follow=False
        )

        self.assertEqual(result.status_code, 200)

    def test_access_as_logout(self):
        self.client.logout()

        result = self.client.get(
            reverse('pages:home'),
            follow=False
        )
        self.assertEqual(result.status_code, 200)


class ContactViewTests(TestCase):

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
            reverse('pages:contact'),
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
            reverse('pages:contact'),
            follow=False
        )

        self.assertEqual(result.status_code, 200)

    def test_access_as_logout(self):
        self.client.logout()

        result = self.client.get(
            reverse('pages:contact'),
            follow=False
        )
        self.assertEqual(result.status_code, 200)


class MissionViewTests(TestCase):

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
            reverse('pages:mission'),
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
            reverse('pages:mission'),
            follow=False
        )

        self.assertEqual(result.status_code, 200)

    def test_access_as_logout(self):
        self.client.logout()

        result = self.client.get(
            reverse('pages:mission'),
            follow=False
        )
        self.assertEqual(result.status_code, 200)


class LogoutViewTests(TestCase):

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
            reverse('pages:logout'),
            follow=True
        )

        self.assertRedirects(
            result,
            reverse('pages:home'),
            status_code=302
        )

    def test_access_as_admin(self):
        self.client.logout()
        self.client.login(
            username=self.admin.username,
            password="passAdmin"
        )

        result = self.client.get(
            reverse('pages:logout'),
            follow=True
        )

        self.assertRedirects(
            result,
            reverse('pages:home'),
            status_code=302
        )

    def test_access_as_logout(self):
        self.client.logout()

        result = self.client.get(
            reverse('pages:logout'),
            follow=True
        )

        self.assertRedirects(
            result,
            reverse('pages:home'),
            status_code=302
        )


class RegisterViewTests(TestCase):

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

    def test_access_as_logout(self):
        self.client.logout()

        result = self.client.get(
            reverse('pages:register'),
            follow=False
        )

        self.assertEqual(result.status_code, 200)

    def test_register_as_logout(self):
        self.client.logout()

        data = {
            'email': 'rignon.noel.1@ens.etsmtl.ca',
            'password': 'ToTo1234#',
        }

        result = self.client.post(
            reverse('pages:register'),
            data,
            follow=True
        )

        self.assertContains(
            result,
            "Un courriel vient de vous être envoyé afin "
            "de valider votre inscription!"
        )

        self.assertRedirects(
            result,
            reverse('pages:home'),
            status_code=302
        )

    def test_bad_email_matricule(self):
        self.client.logout()

        data = {
            'email': 'am56680@ens.etsmtl.ca',
            'password': 'ToTo1234#',
        }

        result = self.client.post(
            reverse('pages:register'),
            data,
            follow=False
        )

        self.assertEqual(result.status_code, 200)

    def test_bad_email_format(self):
        self.client.logout()

        data = {
            'email': 'noel.rignon@ens.etsmtl.ca',
            'password': 'ToTo1234#',
        }

        result = self.client.post(
            reverse('pages:register'),
            data,
            follow=False
        )

        self.assertEqual(result.status_code, 200)

    def test_bad_email_domain(self):
        self.client.logout()

        data = {
            'email': 'noel.rignon.1@etsmtl.ca',
            'password': 'ToTo1234#',
        }

        result = self.client.post(
            reverse('pages:register'),
            data,
            follow=False
        )

        self.assertEqual(result.status_code, 200)


class RegisterValidationViewTests(TestCase):

    def setUp(self):
        settings.EMAIL_BACKEND = \
            'django.core.mail.backends.locmem.EmailBackend'

        self.user = User.objects.create_user(
            username='am56680@ens.etsmtl.ca',
            email='am56680@ens.etsmtl.ca',
            password='passUser',
            is_active=False
        )

    def test_validation_ok(self):
        self.client.logout()
        hash = Hash.objects.create(
            user=self.user,
            hash='toto',
            action='register',
            duration=datetime.timedelta(minutes=30),
        )

        result = self.client.get(
            reverse(
                'pages:register_validation',
                args=[hash.hash]
            ),
            follow=True
        )

        self.assertEqual(result.status_code, 200)

    def test_hash_too_old(self):
        self.client.logout()
        hash = Hash.objects.create(
            user=self.user,
            hash='toto',
            action='register',
            duration=datetime.timedelta(minutes=0),
        )

        result = self.client.get(
            reverse(
                'pages:register_validation',
                args=[hash.hash]
            ),
            follow=True
        )

        self.assertEqual(result.status_code, 200)

    def test_hash_bad_action(self):
        self.client.logout()
        hash = Hash.objects.create(
            user=self.user,
            hash='toto',
            action='toto',
            duration=datetime.timedelta(minutes=30),
        )

        result = self.client.get(
            reverse(
                'pages:register_validation',
                args=[hash.hash]
            ),
            follow=True
        )

        self.assertEqual(result.status_code, 200)

    def test_hash_already_used(self):
        self.client.logout()
        hash = Hash.objects.create(
            user=self.user,
            hash='toto',
            action='register',
            duration=datetime.timedelta(minutes=0),
        )

        # We set the hash as already used
        hash.used = True

        result = self.client.get(
            reverse(
                'pages:register_validation',
                args=[hash.hash]
            ),
            follow=True
        )

        self.assertEqual(result.status_code, 200)

    def test_hash_inexistant(self):
        self.client.logout()

        result = self.client.get(
            reverse(
                'pages:register_validation',
                args=['badHash']
            ),
            follow=True
        )

        self.assertEqual(result.status_code, 200)
