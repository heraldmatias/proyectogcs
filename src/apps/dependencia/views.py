# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from forms import MinisterioForm, OdpForm, GobernacionForm
from django.template import RequestContext
from usuario.models import Usuario, Estado
from models import Ministerio, Odp, Gobernacion
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def ministerio(request):
    profile = Usuario.objects.get(user = request.user)
    if request.method == 'POST':
        num = Ministerio.objects.values("nummin").order_by("-nummin",)[:1]
        num = 1 if len(num)==0 else int(num[0]["nummin"])+1
        iministerio = Ministerio(nummin=num,estado=Estado.objects.get(pk=1),idusuario_creac=profile.numero)
        frmministerio = MinisterioForm(request.POST, instance=iministerio) # A form bound to the POST data
        if frmministerio.is_valid():
            frmministerio.save()
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        frmministerio = MinisterioForm()
    return render_to_response('dependencia/ministerio.html', {'frmministerio': frmministerio,}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def odp(request):
    profile = Usuario.objects.get(user = request.user)
    if request.method == 'POST':
        num = Odp.objects.values("numodp").order_by("-numodp",)[:1]
        num = 1 if len(num)==0 else int(num[0]["numodp"])+1
        iodp = Odp(numodp=num,estado=Estado.objects.get(pk=1),idusuario_creac=profile.numero)
        frmopd = OdpForm(request.POST, instance=iodp) # A form bound to the POST data
        if frmopd.is_valid():
            frmopd.save()
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        frmopd = OdpForm()
    return render_to_response('dependencia/odp.html', {'frmodp': frmopd,}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def gobernacion(request):
    profile = Usuario.objects.get(user = request.user)
    if request.method == 'POST':
        num = Gobernacion.objects.values("numgob").order_by("-numgob",)[:1]
        num = 1 if len(num)==0 else int(num[0]["numgob"])+1
        igobernacion = Gobernacion(numgob=num,estado=Estado.objects.get(pk=1),idusuario_creac=profile.numero)
        frmgobernacion = GobernacionForm(request.POST, instance=igobernacion) # A form bound to the POST data
        if frmgobernacion.is_valid():
            frmgobernacion.save()
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        frmgobernacion = GobernacionForm()
    return render_to_response('dependencia/gobernacion.html', {'frmgobernacion': frmgobernacion,}, context_instance=RequestContext(request),)

