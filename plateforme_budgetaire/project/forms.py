# coding: utf-8

from django import forms
from project.models import Project, SubProject


class ProjectsForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = [
            'author_name',
            'author_website',
            'author_description',
            'name',
            'description',
            'number_affected_by',
            'justification',
            'completion_time',
        ]
        widgets = {
            'author_name': forms.TextInput(),
            'author_website': forms.URLInput(
                attrs={
                    'placeholder': u"https://monSiteEnLigne.ca"
                }
            ),
            'author_description': forms.Textarea(
                attrs={
                    'placeholder': u"Décrivez brievement ici vous ou votre organisation."
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': u"Décrivez ici votre projet: ces enjeux, son avancements, "
                                   u"votre équipe, .."
                }
            ),
            'justification': forms.Textarea(
                attrs={
                    'placeholder': u"Justifiez ici la raison pour laquelle votre projet devrais "
                                   u"être supporter par le CDVU et ce qu'il apporte à la communauté"
                }
            ),
        }


class SubProjectsForm(forms.ModelForm):

    class Meta:
        model = SubProject
        fields = [
            'name',
            'description',
            'completion_time',
            'minimum_amount',
            'maximum_amount',
        ]
        widgets = {
            'name': forms.TextInput(),
            'description': forms.Textarea(
                attrs={
                    'placeholder': u"Décrivez ici votre sous-projet: ces enjeux, son avancements, "
                                   u"votre équipe, .."
                }
            ),
            'completion_time': forms.NumberInput(
                attrs={
                    'placeholder': u"Justifiez ici la raison pour laquelle votre sous-projet devrais "
                                   u"être supporter par le CDVU et ce qu'il apporte à la communauté"
                }
            ),
            'minimum_amount': forms.NumberInput(
                attrs={
                    'placeholder': u"Veuillez entrer un montant minimum pour votre sous-projet"
                }
            ),
            'maximum_amount': forms.NumberInput(
                attrs={
                    'placeholder': u"Veuillez entrer un montant maximum pour votre sous-projet"
                }
            ),
        }
