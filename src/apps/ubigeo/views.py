# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from forms import RegionForm, ProvinciaForm
from dependencia.forms import MinisterioForm, OdpForm, GobernacionForm
from redessociales.forms import InformacionForm, TwitterForm, FacebookForm, TwitterDiarioForm, FacebookDiarioForm
from django.template import RequestContext
from usuario.models import Usuario
from models import Region

def region(request):
    if request.method == 'POST': # If the form has been submitted...
        form = RegionForm(request.POST) # A form bound to the POST data
        #profile = Usuario.objects.get(user = request.user)
        #region = Region.objects.create(
        #region.save()
        if form.is_valid():
            return HttpResponseRedirect('/thanks/') # Redirect after POST        
    frmregion = RegionForm()
    frmprovincia = ProvinciaForm()
    frmministerio = MinisterioForm()
    frmgobernacion = GobernacionForm()
    frmodp = OdpForm()
    frminformacion = InformacionForm() 
    frmtwitter = TwitterForm()
    frmfacebook = FacebookForm
    frmtwitterdiario = TwitterDiarioForm()
    frmfacebookdiario = FacebookDiarioForm()
    print frmregion.errors
    return render_to_response('home/home.html', {'frmregion': frmregion,'frmprovincia':frmprovincia,
    'frmministerio': frmministerio, 'frmgobernacion':frmgobernacion, 'frmodp': frmodp,
    'frminformacion': frminformacion, 'frmtwitter':frmtwitter, 'frmfacebook': frmfacebook,
    'frmtwitterdiario': frmtwitterdiario, 'frmfacebookdiario':frmfacebookdiario,}, context_instance=RequestContext(request),)    
    #return render(request,
            #        'alumno/alumno.html', 
             #       { 'alumno_form' : alumno_form, 'carreras' : carreras, 'conceptos' : conceptos, 'serie_numero':serie_numero})
