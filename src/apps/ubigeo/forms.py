# -*- coding: utf-8 -*-

from django import forms
from models import Region, Provincia
import django_tables2 as tables
from django_tables2.utils import A

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        exclude = ('numreg','idusuario_creac','idusuario_mod',)

class ConsultaRegionForm(forms.Form):
    region = forms.CharField(label="Digite el texto de busqueda:", required=True)

class RegionTable(tables.Table):
    item = tables.Column()
    region = tables.LinkColumn('ogcs-mantenimiento-region-edit', args=[A('numreg')])
    estado = tables.Column()    

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed"}

class ProvinciaForm(forms.ModelForm):
    class Meta:
        model = Provincia
        exclude = ('numpro','estado','idusuario_creac','idusuario_mod',)
