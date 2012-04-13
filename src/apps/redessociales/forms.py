# -*- coding: utf-8 -*-

from django import forms
from models import Informacion, Twitter, TwitterDetalle, TwitterDiario, Facebook, FacebookDetalle, FacebookDiario

class InformacionForm(forms.ModelForm):
    class Meta:
        model = Informacion
        exclude = ('numinf','idusuario_creac','fec_creac','idusuario_mod','fec_mod',)

class TwitterForm(forms.ModelForm):
    class Meta:
        model = Twitter
        #exclude = ('numreg','estado','idusuario_creac','idusuario_mod',)
        widgets = {
            'fechacreac': forms.TextInput(attrs={'id':'id_fechacreac_tw',}),
        }

class FacebookForm(forms.ModelForm):
    class Meta:
        model = Facebook
        #exclude = ('numreg','estado','idusuario_creac','idusuario_mod',)
        widgets = {
            'fechacreac': forms.TextInput(attrs={'id':'id_fechacreac_fb',}),
        }

class TwitterDiarioForm(forms.ModelForm):
    class Meta:
        model = TwitterDiario
        #exclude = ('numreg','estado','idusuario_creac','idusuario_mod',)

class FacebookDiarioForm(forms.ModelForm):
    class Meta:
        model = FacebookDiario
        #exclude = ('numreg','estado','idusuario_creac','idusuario_mod',)
