# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from forms import InformacionForm, TwitterForm, TwitterDetalleForm
from django.template import RequestContext
from usuario.models import Usuario, Estado
from django.contrib.auth.decorators import login_required
from models import Informacion, Twitter, TwitterDetalle
from datetime import datetime

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
    return render_to_response('redes/informacion.html', {'frminformacion': frminformacion,'usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def twitter(request):
    profile = Usuario.objects.get(user = request.user)    
    if request.method == 'POST':  
        num = Twitter.objects.values("numtw").order_by("-numtw",)[:1]
	num = 1 if len(num)==0 else int(num[0]["numtw"])+1
        itwittwer = Twitter(numtw=num,idusuario_creac=profile.numero)
        frmtwitter = TwitterForm(request.POST, instance=itwittwer) # A form bound to the POST data
        if frmtwitter.is_valid():
            frmtwitter.save()
            fechas = request.POST.getlist('tfechas')
            tweets = request.POST.getlist('ttweets')
            siguiendos = request.POST.getlist('tsiguiendo')
            seguidores = request.POST.getlist('tseguidores')
	    for co in range(len(fechas)):
                fecha = fechas[co]
                fecha = datetime.strptime(fecha,"%d/%m/%y").date()
                det = TwitterDetalle(numtw=itwittwer,item=co+1,fechadettw = fecha,tweets=tweets[co],siguiendo =siguiendos[co], seguidores = seguidores[co],)
                det.save() 
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        frmtwitter = TwitterForm()
    frmtwitterdetalle = TwitterDetalleForm()
    return render_to_response('redes/twitter.html', {'frmtwitter': frmtwitter,'frmtwitterdetalle':frmtwitterdetalle,'usuario':request.session['nombres'],'fecha':request.session['login_date']}, context_instance=RequestContext(request),)
