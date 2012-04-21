# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from forms import LoginForm
#from ubigeo.forms import RegionForm, ProvinciaForm
#from dependencia.forms import MinisterioForm, OdpForm, GobernacionForm
#from redessociales.forms import InformacionForm, TwitterForm, FacebookForm, TwitterDiarioForm, FacebookDiarioForm
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
    if 'm' in request.GET:
        return render_to_response('home/home.html',{'m':request.GET['m'],}, context_instance=RequestContext(request),)
    else: 
        return render_to_response('home/home.html', context_instance=RequestContext(request),)

