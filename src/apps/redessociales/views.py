# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from forms import InformacionForm, TwitterForm, TwitterDetalleForm
from django.template import RequestContext
from usuario.models import Usuario, Estado
from django.contrib.auth.decorators import login_required
from models import Informacion, Twitter, TwitterDetalle

@login_required(login_url='/')
def informacion(request):
    profile = Usuario.objects.get(user = request.user)
    if request.method == 'POST':
        num = Informacion.objects.values("numinf").order_by("-numinf",)[:1]
        num = 1 if len(num)==0 else int(num[0]["numinf"])+1
        iinformacion = Informacion(numinf=num,idusuario_creac=profile.numero)
        frminformacion = InformacionForm(request.POST, instance=iinformacion) # A form bound to the POST data
        if frminformacion.is_valid():
            frminformacion.save()
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        frminformacion = InformacionForm()
    return render_to_response('redes/informacion.html', {'frminformacion': frminformacion,}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def twitter(request):
    profile = Usuario.objects.get(user = request.user)    
    if request.method == 'POST':  
        num = Twitter.objects.values("numtw").order_by("-numtw",)[:1]
        num = 1 if len(num)==0 else int(num[0]["numtw"])+1
        fechas = request.POST.getlist('det')
        for det in fechas:
            a=det
        itwittwer = Twitter(numtw=num,idusuario_creac=profile.numero)
        frmtwitter = TwitterForm(request.POST, instance=itwittwer) # A form bound to the POST data
        if frmtwitter.is_valid():
            frmtwitter.save()
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        frmtwitter = TwitterForm()
    frmtwitterdetalle = TwitterDetalleForm()
    return render_to_response('redes/twitter.html', {'frmtwitter': frmtwitter,'frmtwitterdetalle':frmtwitterdetalle,}, context_instance=RequestContext(request),)
