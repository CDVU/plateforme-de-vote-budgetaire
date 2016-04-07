# coding: utf-8

from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import CreateView, TemplateView
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse_lazy
from pages.forms import RegisterForm
from pages.models import Hash
from django.contrib.auth import logout
from django.conf import settings
from django.http import HttpResponseRedirect
import random
import datetime
from django.utils import timezone


def home(request):
    return render(request, 'registration/login.html')


def contact(request):
    return render(request, 'pages/contact.html')


def mission(request):
    return render(request, 'pages/mission.html')


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")


class Register(CreateView):
    model = User
    template_name = 'pages/register.html'
    form_class = RegisterForm
    password = None

    def form_valid(self, form):
        form.instance.username = form.instance.email
        self.password = form.instance.password
        return super(Register, self).form_valid(form)

    def get_success_url(self):
        self.object.set_password(self.password)
        self.object.is_active = False
        self.object.save()

        # Defined the new password
        caractere = "abcdefghijklmnopqrstuvwxyz" \
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
                    "0123456789"

        generate_hash = ""
        for index in range(20):
            generate_hash += random.choice(caractere)

        Hash.objects.create(
            user=self.object,
            hash=generate_hash,
            action='register',
            duration=datetime.timedelta(minutes=30),
        )

        # Send activation email
        self.send_courriel(self.object, generate_hash)

        return reverse_lazy("pages:home")

    def send_courriel(self, user, hash):
        app = settings.CONSTANT
        message = u"Bienvenue sur la plateforme budgétaire du CDVU,\n\n"
        message += u"Pour activer votre compte, veuillez cliquer sur le " \
                   u"lien ci dessous ou copier/coller le lien dans votre " \
                   u"navigateur internet :\n"
        message += u"localhost:8000/register/" + hash
        message += u"\n\n"
        message += u"Pour toute question ou demande d'aide, n'hésitais " \
                   u"pas à nous contacter à l'adresse suivante : "
        message += app['site']['email_technique']

        emailReady = EmailMessage(
            'Bienvenue sur le plateforme budgétaire du CDVU',
            message,
            app['site']['email_technique'],
            [user.email],
            [app['site']['email_technique']],
            reply_to=[app['site']['email_technique']]
        )
        emailReady.send(fail_silently=False)


class RegisterValidation(TemplateView):
    template_name = 'registration/register_validation.html'

    def get_context_data(self, *args, **kwargs):
        context = super(RegisterValidation, self).get_context_data(*args)

        invalid_error = "Ce lien n'est pas valide, une erreure est peut-être survenu! " \
                        "Essayer de recopier votre lien manuellement ou demander en un nouveau."

        datetime_error = "Ce lien n'est plus valide, vous pouvez en demander un" \
                         " nouveau afin d'opérer cette action!"

        used_error = "Ce lien a déjà été utilisé, vous ne pouvez pas effectuer " \
                     "cette action plusieurs fois!"

        try:
            hash = Hash.objects.get(hash=self.args[0])
            if not hash.used:
                if hash.created + hash.duration > timezone.now():
                    if hash.action == 'register':
                        hash.user.is_active = True
                        hash.used = True
                        hash.user.save()
                        hash.save()
                        context['validated'] = True
                    else:
                        context['validated'] = False
                        context['error'] = invalid_error
                else:
                    context['validated'] = False
                    context['error'] = datetime_error
            else:
                context['validated'] = False
                context['error'] = used_error
        except:
            context['validated'] = False
            context['error'] = invalid_error

        return context
