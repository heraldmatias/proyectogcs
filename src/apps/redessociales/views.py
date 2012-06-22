# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from forms import InformacionForm, TwitterForm, TwitterDetalleForm, FacebookForm, FacebookDetalleForm,FacebookDiarioForm, TwitterDiarioForm
from django.template import RequestContext
from usuario.models import Usuario, Estado
from django.contrib.auth.decorators import login_required
from models import Informacion, Twitter, TwitterDetalle, Facebook, FacebookDetalle, TwitterDiario, FacebookDiario
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
    return render_to_response('redes/informacion.html', {'frminformacion': frminformacion,'opcion':'add'}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def twitter(request): 
    if request.method == 'POST':  
        num = Twitter.objects.values("numtw").order_by("-numtw",)[:1]
	num = 1 if len(num)==0 else int(num[0]["numtw"])+1
        profile = Usuario.objects.get(user = request.user)
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
    return render_to_response('redes/twitter.html', {'frmtwitter': frmtwitter,'frmtwitterdetalle':frmtwitterdetalle,'opcion':'add'}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def facebook(request):   
    if request.method == 'POST':  
        num = Facebook.objects.values("numfb").order_by("-numfb",)[:1]
	num = 1 if len(num)==0 else int(num[0]["numfb"])+1
        profile = Usuario.objects.get(user = request.user) 
        ifacebook = Facebook(numfb=num,idusuario_creac=profile.numero)
        frmfacebook = FacebookForm(request.POST, instance=ifacebook) # A form bound to the POST data
        if frmfacebook.is_valid():
            frmfacebook.save()
            fechas = request.POST.getlist('tfechas')
            likes = request.POST.getlist('tlikes')
	    for co in range(len(fechas)):
                fecha = fechas[co]
                fecha = datetime.strptime(fecha,"%d/%m/%y").date()
                det = FacebookDetalle(numfb=ifacebook,item=co+1,fechadetfb = fecha,cantidad=likes[co],)
                det.save() 
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        frmfacebook = FacebookForm()
    frmfacebookdetalle = FacebookDetalleForm()
    return render_to_response('redes/facebook.html', {'frmfacebook': frmfacebook,'frmfacebookdetalle':frmfacebookdetalle,'opcion':'add'}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def facebookdiario(request):   
    if request.method == 'POST':  
        num = FacebookDiario.objects.values("numfbdia").order_by("-numfbdia",)[:1]
	num = 1 if len(num)==0 else int(num[0]["numfbdia"])+1
        profile = Usuario.objects.get(user = request.user) 
        ifacebook = FacebookDiario(numfbdia=num,idusuario_creac=profile.numero)
        frmfacebookdiario = FacebookDiarioForm(request.POST, instance=ifacebook) # A form bound to the POST data
        if frmfacebookdiario.is_valid():
            frmfacebookdiario.save()
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        frmfacebookdiario = FacebookDiarioForm()
    return render_to_response('redes/facebookdiario.html', {'frmfacebookdiario': frmfacebookdiario,'opcion':'add',}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def twitterdiario(request):
    if request.method == 'POST':  
        num = TwitterDiario.objects.values("numtwdia").order_by("-numtwdia",)[:1]
	num = 1 if len(num)==0 else int(num[0]["numtwdia"])+1
        profile = Usuario.objects.get(user = request.user) 
        itwittwer = TwitterDiario(numtwdia=num,idusuario_creac=profile.numero)
        frmtwitterdiario = TwitterDiarioForm(request.POST, instance=itwittwer) # A form bound to the POST data
        if frmtwitterdiario.is_valid():
            frmtwitterdiario.save()
            return redirect('/home/') # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        frmtwitterdiario = TwitterDiarioForm()
    return render_to_response('redes/twitterdiario.html', {'frmtwitterdiario': frmtwitterdiario,'opcion':'add'}, context_instance=RequestContext(request),)
