# coding: utf-8

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


my_validator = RegexValidator(
    r"^[a-z\-]+\.[a-z\-]+.[0-9]+@ens.etsmtl.ca$",
    u"Votre email doit être du style prenom.nom.2@ens.etsmtl.ca."
)


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

    email = forms.CharField(
        label=_('Email'),
        required=True,
        max_length=100,
        validators=[my_validator]
    )
    email.widget.attrs.update({
            'placeholder': _(u'prenom.nom.2@ens.etsmtl.ca'),
            'class': 'form-control'
    })

    password = forms.CharField(
        label=_('Password'),
        required=True,
        max_length=100
    )
    password.widget.attrs.update({
        'placeholder': _(u'********'),
        'class': 'form-control',
        'type': 'hidden'
    })
