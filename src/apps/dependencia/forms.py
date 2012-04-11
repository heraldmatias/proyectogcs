# -*- coding: utf-8 -*-

from django import forms
from models import Ministerio, Odp, Gobernacion

class MinisterioForm(forms.ModelForm):
    class Meta:
        model = Ministerio
        #exclude = ('numreg','estado','idusuario_creac','idusuario_mod',)

class OdpForm(forms.ModelForm):
    class Meta:
        model = Odp
        #exclude = ('numreg','estado','idusuario_creac','idusuario_mod',)

class GobernacionForm(forms.ModelForm):
    class Meta:
        model = Gobernacion
        #exclude = ('numreg','estado','idusuario_creac','idusuario_mod',)
