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
        label=_('Courriel'),
        required=True,
        max_length=100,
        validators=[my_validator]
    )
    email.widget.attrs.update({
            'placeholder': _(u'prenom.nom.2@ens.etsmtl.ca'),
            'class': 'form-control'
    })

    password = forms.CharField(
        label=_('Mot de passe'),
        required=True,
        max_length=100,
        widget=forms.PasswordInput
    )
    password.widget.attrs.update({
        'placeholder': _(u'********'),
        'class': 'form-control',
    })

    password_verify = forms.CharField(
        label=_(u'Vérification'),
        required=False,
        max_length=100,
        widget=forms.PasswordInput
    )
    password_verify.widget.attrs.update({
        'placeholder': _(u'********'),
        'class': 'form-control',
    })

    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password_verify')
        email = self.cleaned_data.get('email')

        if User.objects.filter(username=email).count():
            raise forms.ValidationError("Ce courriel est déjà utilisé !")

        if password1 and password1 != password2:
            raise forms.ValidationError(
                "Les mots de passe ne sont pas identiques !"
            )

        return self.cleaned_data
