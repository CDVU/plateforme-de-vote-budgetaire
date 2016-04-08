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
                    'placeholder': u"Décrivez brievement ici vous ou votre "
                                   u"organisation."
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': u"Décrivez ici votre projet: ces enjeux, "
                                   u"son avancements, votre équipe, .."
                }
            ),
            'justification': forms.Textarea(
                attrs={
                    'placeholder': u"Justifiez ici la raison pour laquelle "
                                   u"votre projet devrais être supporter "
                                   u"par le CDVU et ce qu'il apporte à la "
                                   u"communauté"
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
                    'placeholder': u"Décrivez ici votre sous-projet: ces "
                                   u"enjeux, son avancements, votre équipe, "
                                   u".."
                }
            ),
            'completion_time': forms.NumberInput(
                attrs={
                    'placeholder': u"Justifiez ici la raison pour laquelle "
                                   u"votre sous-projet devrais être "
                                   u"supporter par le CDVU et ce qu'il "
                                   u"apporte à la communauté"
                }
            ),
            'minimum_amount': forms.NumberInput(
                attrs={
                    'placeholder': u"Veuillez entrer un montant minimum "
                                   u"pour votre sous-projet"
                }
            ),
            'maximum_amount': forms.NumberInput(
                attrs={
                    'placeholder': u"Veuillez entrer un montant maximum "
                                   u"pour votre sous-projet"
                }
            ),
        }
