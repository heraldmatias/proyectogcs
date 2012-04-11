# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from forms import LoginForm
from ubigeo.forms import RegionForm, ProvinciaForm
from dependencia.forms import MinisterioForm, OdpForm, GobernacionForm
from redessociales.forms import InformacionForm, TwitterForm, FacebookForm, TwitterDiarioForm, FacebookDiarioForm
#from dependencia.forms import ProvinciaForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

def index(request):
    form = LoginForm()
    return render_to_response('home/index.html', {'form': form,}, context_instance=RequestContext(request),)

def singin(request):
    username = request.POST['usuario']
    password = request.POST['clave']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('/home/')
    else:
        form = LoginForm()
        return render(request,
                        "home/index.html",
                        {"error_message":"Por favor ingrese valores correctos.",'form':form,})

@login_required(login_url='/')
def main(request):
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
    return render_to_response('home/home.html', {'frmregion': frmregion,'frmprovincia':frmprovincia,
    'frmministerio': frmministerio, 'frmgobernacion':frmgobernacion, 'frmodp': frmodp,
    'frminformacion': frminformacion, 'frmtwitter':frmtwitter, 'frmfacebook': frmfacebook,
    'frmtwitterdiario': frmtwitterdiario, 'frmfacebookdiario':frmfacebookdiario,}, context_instance=RequestContext(request),)

