# -*- coding: utf-8 -*-

from django import forms
from models import Ministerio, Odp, Gobernacion
import django_tables2 as tables
from django_tables2.utils import A

class MinisterioForm(forms.ModelForm):
    class Meta:
        model = Ministerio
        fields = ('ministerio','iniciales','estado')

class ConsultaMinisterioForm(forms.Form):
    ministerio = forms.CharField(label="Digite el texto de busqueda:", required=False)

class MinisterioTable(tables.Table):
    item = tables.Column()
    ministerio = tables.LinkColumn('ogcs-mantenimiento-ministerio-edit', args=[A('nummin')],orderable=True)
    estado = tables.Column()    

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed"}
        orderable = False


class OdpForm(forms.ModelForm):
    class Meta:
        model = Odp
        fields = ('nummin','odp','iniciales','estado')

class ConsultaOdpForm(forms.ModelForm):
    class Meta:
        model = Odp
        fields = ('nummin','odp',)

class OdpTable(tables.Table):
    item = tables.Column()
    nummin = tables.Column()
    odp = tables.LinkColumn('ogcs-mantenimiento-odp-edit', args=[A('numodp')],orderable=True)
    iniciales = tables.Column()
    estado = tables.Column()    

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed"}
        orderable = False

class GobernacionForm(forms.ModelForm):
    class Meta:
        model = Gobernacion
        fields = ('region','provincia','gobernacion','iniciales','estado')
        widgets = {
            'region': forms.Select(attrs={'onChange':'provincias();',}),
        }

class ConsultaGobernacionForm(forms.ModelForm):
    class Meta:
        model = Gobernacion
        fields = ('region','provincia',)
        widgets = {
            'region': forms.Select(attrs={'onChange':'provincias();',}),
        }

class GobernacionTable(tables.Table):
    item = tables.Column()
    region = tables.Column()
    provincia = tables.Column()
    gobernacion = tables.LinkColumn('ogcs-mantenimiento-gobernacion-edit', args=[A('numgob')],orderable=True)
    iniciales = tables.Column()
    estado = tables.Column()    

    def render_item(self):
        value = getattr(self, '_counter', 1)
        self._counter = value + 1
        return '%d' % value

    class Meta:
        attrs = {"class": "table table-bordered table-condensed"}
        orderable = False
