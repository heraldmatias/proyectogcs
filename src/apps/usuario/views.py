# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from forms import UsuarioForm
from django.template import RequestContext
from usuario.models import Usuario, Estado
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def usuario(request):
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
