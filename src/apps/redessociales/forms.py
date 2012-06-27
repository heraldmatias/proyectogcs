# -*- coding: utf-8 -*-

from django import forms
from models import Informacion, Twitter, TwitterDetalle, TwitterDiario, Facebook, FacebookDetalle, FacebookDiario
import django_tables2 as tables 
from django.utils.safestring import mark_safe
from usuario.models import Organismo
class InformacionForm(forms.ModelForm):
    class Meta:
        model = Informacion
        exclude = ('organismo','dependencia','numinf','idusuario_creac','fec_creac','idusuario_mod','fec_mod',)
        
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
        exclude = ('dependencia','organismo','numtw','idusuario_creac','fec_creac','idusuario_mod','fec_mod','idadministrador_mod','fec_modadm')
        widgets = {
            'fechacreac': forms.TextInput(attrs={'id':'id_fechacreac_tw','style':'width:100px;','readonly':'readonly','data-date-format':'dd/mm/yyyy'}),            
        }

class TwitterConsultaForm(forms.ModelForm):
    class Meta:
        model = Twitter
        fields = ('organismo','dependencia',)
        widgets = {
            'dependencia': forms.Select(),
            'organismo': forms.Select(attrs={'onChange':'dependencias();',}),
        }

class TwitterTable(tables.Table):
    item = tables.Column()
    organismo = tables.Column(orderable=True)
    dependencia = tables.Column(orderable=True)
    idusuario_creac = tables.Column(verbose_name='Creador',orderable=True)
    fec_creac = tables.Column(verbose_name='Fec. Creación',orderable=True)
    idusuario_mod = tables.Column(verbose_name='Modificador',orderable=True)
    fec_mod = tables.Column(verbose_name='Fec. Modificador',orderable=True)
    modificar = tables.TemplateColumn('<a href={% url ogcs-redes-twitter-edit record.numtw %}>Modificar</a>')
    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False

class TwitterDetalleForm(forms.ModelForm):
    class Meta:
        model = TwitterDetalle
        exclude = ('numtw','item','auditoria',)        
        widgets = {
            'tweets': forms.TextInput(attrs={'class':'span1'}),
            'siguiendo': forms.TextInput(attrs={'class':'span1'}),
            'seguidores': forms.TextInput(attrs={'class':'span1'}),
            'fechadettw': forms.TextInput(attrs={'style':'width:100px;','readonly':'readonly'}),
        }

class DetalleTwitterTable(tables.Table):
    item = tables.Column()    
    fechadettw = tables.TemplateColumn('<input type="hidden" name="tfechas" value="{{ record.fechadettw }}">{{ record.fechadettw }}')
    tweets = tables.TemplateColumn('<input type="hidden" name="ttweets" value="{{ record.tweets }}">{{ record.tweets }}')
    siguiendo = tables.TemplateColumn('<input type="hidden" name="tsiguiendo" value="{{ record.siguiendo }}">{{ record.siguiendo }}')
    seguidores = tables.TemplateColumn('<input type="hidden" name="tseguidores" value="{{ record.seguidores }}">{{ record.seguidores }}')
    eliminar = tables.Column()
    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    def render_eliminar(self):
        value = getattr(self, '_co', 1) 
        self._co = value + 1       
        return mark_safe("<a href='javascript: removedetalle(%s)'><div id='delete'></div></a>"%str(value))

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped",'id':'tbldetalle'}
        orderable = False

class TwitterDiarioForm(forms.ModelForm):
    class Meta:
        model = TwitterDiario
        exclude = ('organismo','dependencia','numtwdia','idusuario_creac','fec_creac','idusuario_mod','fec_mod','idadministrador_mod','fec_modadm')

class TwitterDiarioConsultaForm(forms.Form):
    organismo = forms.ModelChoiceField(queryset=Organismo.objects.all(),widget=forms.Select(attrs={'onChange':'dependencias(1);'}))
    dependencia = forms.ChoiceField(choices=[])
    fecini = forms.CharField()
    fecfin = forms.CharField()
       
       
class TwitterDiarioTable(tables.Table):
    item = tables.Column()
    organismo = tables.Column(orderable=True)
    dependencia = tables.Column(orderable=True)
    fechacreacdia = tables.Column(orderable=True)
    actividad = tables.Column(orderable=True)
    totaltweets = tables.Column(orderable=True)
    totalretweets = tables.Column(orderable=True)
    idusuario_creac = tables.Column(verbose_name='Creador',orderable=True)
    fec_creac = tables.Column(verbose_name='Fec. Creación',orderable=True)
    idusuario_mod = tables.Column(verbose_name='Modificador',orderable=True)
    fec_mod = tables.Column(verbose_name='Fec. Modificador',orderable=True)
    modificar = tables.TemplateColumn('<a href={% url ogcs-redes-twitter-diario-edit record.numtwdia %}>Modificar</a>')
    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed table-striped"}
        orderable = False

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

class FacebookDiarioForm(forms.ModelForm):
    class Meta:
        model = FacebookDiario
        exclude = ('numfbdia','idusuario_creac','idusuario_mod','fec_mod','fec_modadm','idadministrador_mod')
        widgets = {
            'dependencia': forms.Select(),
            'organismo': forms.Select(attrs={'onChange':'dependencias();',}),
        }
