# -*- coding: utf-8 -*-

from django import forms
from models import Region, Provincia

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        exclude = ('numreg','estado','idusuario_creac','idusuario_mod',)

class ProvinciaForm(forms.ModelForm):
    class Meta:
        model = Provincia
        exclude = ('numpro','estado','idusuario_creac','idusuario_mod',)
