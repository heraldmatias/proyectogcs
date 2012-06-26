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

class InformacionConsultaForm(forms.ModelForm):
    class Meta:
        model = Informacion
        fields = ('organismo','dependencia',)
        widgets = {
            'dependencia': forms.Select(),
            'organismo': forms.Select(attrs={'onChange':'dependencias();',}),
        }

class InformacionTable(tables.Table):
    item = tables.Column()
    organismo = tables.Column(orderable=True)
    dependencia = tables.Column(orderable=True)
    idusuario_creac = tables.Column(orderable=True)
    fec_creac = tables.Column(orderable=True)
    idusuario_mod = tables.Column(orderable=True)
    fec_mod = tables.Column(orderable=True)
    modificar = tables.TemplateColumn('<a href={% url ogcs-redes-informacion-edit record.numinf %}>Modificar</a>')
    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False

class TwitterForm(forms.ModelForm):
    class Meta:
        model = Twitter
        exclude = ('numtw','idusuario_creac','fec_creac','idusuario_mod','fec_mod','idadministrador_mod','fec_modadm')
        widgets = {
            'fechacreac': forms.TextInput(attrs={'id':'id_fechacreac_tw','readonly':'readonly'}),
            'dependencia': forms.Select(),
            'organismo': forms.Select(attrs={'onChange':'dependencias();',}),
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
        exclude = ('numfb','estado','idusuario_creac','idusuario_mod','fec_mod','idadministrador_mod','fec_modadm')
        widgets = {
            'fechacreac': forms.TextInput(attrs={'id':'id_fechacreac_fb',}),
            'dependencia': forms.Select(),
            'organismo': forms.Select(attrs={'onChange':'dependencias();',}),
        }

class FacebookDetalleForm(forms.ModelForm):
    class Meta:
        model = FacebookDetalle
        exclude = ('numfb','item','auditoria',)        
        widgets = {
            'cantidad': forms.TextInput(attrs={'class':'span1'}),
            'fechadetfb': forms.TextInput(attrs={'class':'span1'}),
        }
class TwitterDiarioForm(forms.ModelForm):
    class Meta:
        model = TwitterDiario
        exclude = ('numtwdia','idusuario_creac',)
        widgets = {
            'dependencia': forms.Select(),
            'organismo': forms.Select(attrs={'onChange':'dependencias();',}),
        }
class FacebookDiarioForm(forms.ModelForm):
    class Meta:
        model = FacebookDiario
        exclude = ('numfbdia','idusuario_creac','idusuario_mod','fec_mod','fec_modadm','idadministrador_mod')
        widgets = {
            'dependencia': forms.Select(),
            'organismo': forms.Select(attrs={'onChange':'dependencias();',}),
        }
