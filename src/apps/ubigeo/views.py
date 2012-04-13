# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from forms import RegionForm, ProvinciaForm
from django.template import RequestContext
from usuario.models import Usuario, Estado
from models import Region, Provincia
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse

@login_required(login_url='/')
def region(request):
    profile = Usuario.objects.get(user = request.user)
    if request.method == 'POST':
        num = Region.objects.values("numreg").order_by("-numreg",)[:1]
        num = 1 if len(num)==0 else int(num[0]["numreg"])+1
        region = Region(numreg=num,estado=Estado.objects.get(pk=1),idusuario_creac=profile.numero)
        frmregion = RegionForm(request.POST, instance=region) # A form bound to the POST data
        if frmregion.is_valid():
            frmregion.save()
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        frmregion = RegionForm()
    return render_to_response('ubigeo/region.html', {'frmregion': frmregion,}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def provincia(request):
    profile = Usuario.objects.get(user = request.user)
    if request.method == 'POST':
        num = Provincia.objects.values("numpro").order_by("-numpro",)[:1]
        num = 1 if len(num)==0 else int(num[0]["numpro"])+1
        provincia = Provincia(numpro=num,estado=Estado.objects.get(pk=1),idusuario_creac=profile.numero)
        frmprovincia = ProvinciaForm(request.POST, instance=provincia) # A form bound to the POST data
        if frmprovincia.is_valid():
            frmprovincia.save()
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        frmprovincia = ProvinciaForm()
    return render_to_response('ubigeo/provincia.html', {'frmprovincia': frmprovincia,}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def jsonprovincia(request):
    provincias = Provincia.objects.filter(region = Region.objects.get(numreg = request.GET['r'])).order_by('provincia')
    return HttpResponse(serializers.serialize("json", provincias, ensure_ascii=False),mimetype='application/json')
