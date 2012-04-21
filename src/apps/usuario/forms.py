# -*- coding: utf-8 -*-

from django import forms
from models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        exclude = ('idusuario_mod','fec_mod','user','numero')
        widgets = {
            'dependencia': forms.Select(),
            'organismo': forms.Select(attrs={'onChange':'dependencias();',}),
            'contrasena': forms.PasswordInput(),
        }
