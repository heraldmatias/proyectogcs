# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from forms import RegionForm, ProvinciaForm
from django.template import RequestContext
from usuario.models import Usuario, Estado
from models import Region

def region(request):
    profile = Usuario.objects.get(user = request.user)
    if request.method == 'POST': # If the form has been submitted...
        region = Region(numreg=4,estado=Estado.objects.get(pk=1),idusuario_creac=profile.numero)        
        frmregion = RegionForm(request.POST, instance=region) # A form bound to the POST data
        #region = Region.objects.create(
        if frmregion.is_valid():
            frmregion.save()
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        frmregion = RegionForm()
    return render_to_response('ubigeo/region.html', {'frmregion': frmregion,}, context_instance=RequestContext(request),)