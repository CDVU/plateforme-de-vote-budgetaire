from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

    email = forms.CharField(
        label=_('Email'),
        required=True,
        max_length=100
    )
    email.widget.attrs.update({'placeholder': _(u'AB12345@ens.etsmtl.ca'), 'class': 'form-control'})
