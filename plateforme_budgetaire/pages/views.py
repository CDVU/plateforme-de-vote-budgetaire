# coding: utf-8

from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse_lazy
from pages.forms import RegisterForm
import random

from django.conf import settings


def home(request):
    return render(request, 'pages/home.html')


def contact(request):
    return render(request, 'pages/contact.html')


class Register(CreateView):
    model = User
    template_name = 'pages/register.html'
    form_class = RegisterForm

    def get_success_url(self):
        user = self.object
        user.username = user.email

        # Defined the new password
        caractere = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        password = ""
        for index in range(10):
            password += random.choice(caractere)

        user.set_password(password)
        user.save()

        # Send verification email
        # self.send_courriel(user, password)

        return reverse_lazy("pages:home")

    def send_courriel(self, user, password):
        app = settings.CONSTANT
        message = u"Un compte vient de vous être créé pour accéder à la plateforme budgétaire du CDVU. Vous pouvez dès maintenant vous y connecter avec les identifiants suivants : \n\n"
        message += u"Username : "
        message += user.username
        message += u"\n"
        message += u"Password : "
        message += password
        message += u"\n"
        message += u"Lien : "
        message += app['site']['dns']
        message += u"\n\n\n"
        message += u"Pour toute question ou demande d'aide, n'hésitais pas à nous contacter à l'adresse suivante : "
        message += app['site']['email_technique']
        message += u"\n\n"
        message += u"Nous vous souhaitons une agréable journée!"
        message += u"\n\n"
        message += u"----------------------------------------\n\n"
        message += u"Ce message du CDVU est un élément important d'un programme auquel vous participer. Si ce n'est pas le cas veuillez nous en excuser et effacer ce message.\n"
        message += u"Si nous persistons à vous envoyer des courriel sans votre accord, contacter nous à l'adresse suivante : "
        message += app['site']['email_technique']

        emailReady = EmailMessage('Bienvenue sur le plateforme budgétaire du CDVU', message, app['site']['email_technique'],
            [user.email], [app['site']['email_technique']],
            reply_to=[app['site']['email_technique']])
        emailReady.send(fail_silently=False)