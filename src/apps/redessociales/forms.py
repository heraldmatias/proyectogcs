# -*- coding: utf-8 -*-

from django import forms
from models import Informacion, Twitter, TwitterDetalle, TwitterDiario, Facebook, FacebookDetalle, FacebookDiario
import django_tables2 as tables 

class InformacionForm(forms.ModelForm):
    class Meta:
        model = Informacion
        exclude = ('numinf','idusuario_creac','fec_creac','idusuario_mod','fec_mod',)
        widgets = {
            'dependencia': forms.Select(),
            'organismo': forms.Select(attrs={'onChange':'dependencias();',}),
        }

class TwitterForm(forms.ModelForm):
    class Meta:
        model = Twitter
        exclude = ('numtw','idusuario_creac','fec_creac','idusuario_mod','fec_mod','idadministrador_mod','fec_modadm')
        widgets = {
            'fechacreac': forms.TextInput(attrs={'id':'id_fechacreac_tw','readonly':'readonly'}),
        }

class TwitterDetalleForm(forms.ModelForm):
    class Meta:
        model = TwitterDetalle
        exclude = ('numtw','item','auditoria',)        
        widgets = {
            'tweets': forms.TextInput(attrs={'class':'span1'}),
            'siguiendo': forms.TextInput(attrs={'class':'span1'}),
            'seguidores': forms.TextInput(attrs={'class':'span1'}),
            'fechadettw': forms.TextInput(attrs={'class':'span1'}),
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
