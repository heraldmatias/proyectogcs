# -*- coding: utf-8 -*-

from django import forms
from models import Ministerio, Odp, Gobernacion

class MinisterioForm(forms.ModelForm):
    class Meta:
        model = Ministerio
        fields = ('ministerio','iniciales',)

class OdpForm(forms.ModelForm):
    class Meta:
        model = Odp
        fields = ('nummin','odp','iniciales',)

class GobernacionForm(forms.ModelForm):
    class Meta:
        model = Gobernacion
        fields = ('region','provincia','gobernacion','iniciales',)
        widgets = {
            'region': forms.Select(attrs={'onChange':'provincias();',}),
        }
