# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from forms import InformacionForm, TwitterForm, TwitterDetalleForm, FacebookForm, FacebookDetalleForm,FacebookDiarioForm, TwitterDiarioForm,InformacionConsultaForm, InformacionTable, DetalleTwitterTable, TwitterConsultaForm, TwitterTable,TwitterDiarioConsultaForm, TwitterDiarioTable
from django.template import RequestContext
from usuario.models import Usuario, Estado
from django.contrib.auth.decorators import login_required
from models import Informacion, Twitter, TwitterDetalle, Facebook, FacebookDetalle, TwitterDiario, FacebookDiario
from datetime import datetime
from django_tables2.config import RequestConfig
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from scripts.scripts import imprimirToPDF
from django.template.loader import render_to_string

@login_required()
def informacion(request):
    mensaje = ''
    dependencia= None
    if request.method == 'POST':
        usuario = request.user.get_profile()
        num = Informacion.objects.values("numinf").order_by("-numinf",)[:1]
        num = 1 if len(num)==0 else int(num[0]["numinf"])+1
        iinformacion = Informacion(numinf=num,idusuario_creac=usuario,organismo=usuario.organismo,dependencia=usuario.dependencia)
        frminformacion = InformacionForm(request.POST, instance=iinformacion) # A form bound to the POST data
        dependencia = usuario.dependencia
        if frminformacion.is_valid():
            frminformacion.save()
            mensaje = 'Registro grabado satisfactoriamente'
            frminformacion = InformacionForm()
    else:        
        frminformacion = InformacionForm()
    return render_to_response('redes/informacion.html', {'formulario': frminformacion,'opcion':'add','mensaje':mensaje,'dependencia':dependencia,}, context_instance=RequestContext(request),)

@login_required()
def informacion_edit(request, codigo):
    if request.method == 'POST':
        info = get_object_or_404(Informacion, numinf=int(codigo))  
        info.idusuario_mod = request.user.get_profile()
        info.fec_mod = datetime.now()
        dependencia = info.dependencia
        formulario = InformacionForm(request.POST, instance=info) # A form bound to the POST data
        if formulario.is_valid():
            formulario.save()
            return redirect(reverse('ogcs-redes-informacion-query')+'?m=edit') # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        info = get_object_or_404(Informacion, numinf=int(codigo))        
        dependencia = info.dependencia
        formulario = InformacionForm(instance=info)
    return render_to_response('redes/informacion.html', {'formulario': formulario,'opcion':'edit','codigo':codigo,'dependencia':dependencia,}, context_instance=RequestContext(request),)

@login_required()
def informacion_consulta(request):
    filtro = []
    mensaje = request.GET['m'] if 'm' in request.GET else None
    dependencia= None
    #filtros
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u'organismo_id=%s'%request.GET['organismo'])   
    if 'dependencia' in request.GET:
        if request.GET['dependencia']:
            filtro.append(u'dependencia=%s'%request.GET['dependencia'])
            dependencia = request.GET['dependencia']
    formulario = InformacionConsultaForm(request.GET)
    query = Informacion.objects.extra(where=filtro, select={'dependencia':"case organismo_id when 1 then (select ministerio from ministerio where nummin=dependencia) when 2 then (select odp from odp where numodp=dependencia) when 3 then (select gobernacion from gobernacion where numgob=dependencia) end"})
    tabla = InformacionTable(query)
    RequestConfig(request).configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('redes/informacion_consulta.html',{'formulario':formulario,'tabla':tabla,'dependencia':dependencia,'mensaje':mensaje},context_instance=RequestContext(request))

@login_required()
def informacion_print(request):
    filtro = []
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u'organismo_id=%s'%request.GET['organismo'])   
    if 'dependencia' in request.GET:
        if request.GET['dependencia']:
            filtro.append(u'dependencia=%s'%request.GET['dependencia'])
    query = Informacion.objects.extra(where=filtro, select={'dependencia':"case organismo_id when 1 then (select ministerio from ministerio where nummin=dependencia) when 2 then (select odp from odp where numodp=dependencia) when 3 then (select gobernacion from gobernacion where numgob=dependencia) end",'encargado':"concat(nombresenc,' ',apellidosenc)",'jefe':"concat(nombresjefe,' ',apellidosjefe)"})
    html = render_to_string('redes/informacion_reporte.html',{'data': query,'pagesize':'A4','usuario':request.user.get_profile()},context_instance=RequestContext(request))
    filename= "informacion_%s.pdf" % datetime.today().strftime("%Y%m%d")        
    return imprimirToPDF(html,filename)

@login_required(login_url='/')
def twitter(request): 
    mensaje = ''
    if request.method == 'POST':  
        num = Twitter.objects.values("numtw").order_by("-numtw",)[:1]
	num = 1 if len(num)==0 else int(num[0]["numtw"])+1
        profile = request.user.get_profile()
        itwittwer = Twitter(numtw=num,idusuario_creac=profile,organismo=profile.organismo,dependencia=profile.dependencia)
        frmtwitter = TwitterForm(request.POST, instance=itwittwer) # A form bound to the POST data
        if frmtwitter.is_valid():
            frmtwitter.save()
            fechas = request.POST.getlist('tfechas')
            tweets = request.POST.getlist('ttweets')
            siguiendos = request.POST.getlist('tsiguiendo')
            seguidores = request.POST.getlist('tseguidores')
	    for co in range(len(fechas)):
                fecha = fechas[co]                
                fecha = datetime.strptime(fecha,"%d/%m/%Y")
                det = TwitterDetalle(numtw=itwittwer,item=co+1,fechadettw = fecha,tweets=tweets[co],siguiendo =siguiendos[co], seguidores = seguidores[co],)
                det.save() 
            mensaje = 'Registro grabado satisfactoriamente'
            frmtwitter = TwitterForm()
    else:        
        frmtwitter = TwitterForm()
    frmtwitterdetalle = TwitterDetalleForm()
    tabla = DetalleTwitterTable([])
    return render_to_response('redes/twitter.html', {'formulario': frmtwitter,'frm_detalle':frmtwitterdetalle,'opcion':'add','tabla':tabla,'mensaje':mensaje}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def twitter_edit(request, codigo): 
    mensaje = ''
    if request.method == 'POST':  
        itwitter = get_object_or_404(Twitter,pk=codigo)
        profile = request.user.get_profile()
        if profile.nivel.codigo == 1:
            itwitter.fec_mod = datetime.now()
            itwitter.idusuario_mod = profile
        else:
            itwitter.idadministrador_mod = profile
            itwitter.fec_modadm = datetime.now()      
        frmtwitter = TwitterForm(request.POST, instance=itwitter)  
        if frmtwitter.is_valid():
            frmtwitter.save()
            fechas = request.POST.getlist('tfechas')
            tweets = request.POST.getlist('ttweets')
            siguiendos = request.POST.getlist('tsiguiendo')
            seguidores = request.POST.getlist('tseguidores')
	    #TWITTER_DETALLE_save
            query = TwitterDetalle.objects.filter(numtw=itwitter)
            for c in range(len(tweets)):
                fecha = datetime.strptime(fechas[c],"%d/%m/%Y")
                try:
                    row = TwitterDetalle.objects.get(numtw=itwitter,item=c+1)
                    row.fechadettw = fecha
                    row.tweets = tweets[c]
                    row.siguiendo = siguiendos[c]
                    row.siguidores = seguidores[c]
                    row.save()
                except TwitterDetalle.DoesNotExist:
                    TwitterDetalle(numtw=itwitter,item=c+1,fechadettw = fecha,tweets=tweets[c],siguiendo =siguiendos[c], seguidores = seguidores[c],).save()
            resto= len(tweets)
            while resto < len(query):
                row = TwitterDetalle.objects.get(numtw=itwitter,item=resto+1)
                row.delete()
                resto = resto + 1
            return redirect(reverse('ogcs-redes-twitter-query')+'?m=edit') 
    else: 
        itwitter = get_object_or_404(Twitter,pk=codigo)
        itwitter.fechacreac = itwitter.fechacreac.strftime("%d/%m/%Y")       
        frmtwitter = TwitterForm(instance = itwitter)
    detalle = TwitterDetalle.objects.filter(numtw=itwitter)#.order_by('-fechadettw')
    for row in detalle:
        row.fechadettw = row.fechadettw.strftime("%d/%m/%Y")
    tabla = DetalleTwitterTable(detalle)
    frmtwitterdetalle = TwitterDetalleForm()
    return render_to_response('redes/twitter.html', {'formulario': frmtwitter,'frm_detalle':frmtwitterdetalle,'opcion':'edit','codigo':codigo,'tabla':tabla}, context_instance=RequestContext(request),)

@login_required()
def twitter_consulta(request):
    filtro = []
    mensaje = request.GET['m'] if 'm' in request.GET else None
    dependencia= None
    #filtros
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u'organismo_id=%s'%request.GET['organismo'])   
    if 'dependencia' in request.GET:
        if request.GET['dependencia']:
            filtro.append(u'dependencia=%s'%request.GET['dependencia'])
            dependencia = request.GET['dependencia']
    formulario = TwitterConsultaForm(request.GET)
    query = Twitter.objects.extra(where=filtro, select={'dependencia':"case organismo_id when 1 then (select ministerio from ministerio where nummin=dependencia) when 2 then (select odp from odp where numodp=dependencia) when 3 then (select gobernacion from gobernacion where numgob=dependencia) end"})
    tabla = TwitterTable(query)
    RequestConfig(request).configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('redes/twitter_consulta.html',{'formulario':formulario,'tabla':tabla,'dependencia':dependencia,'mensaje':mensaje},context_instance=RequestContext(request))

@login_required()
def twitter_print(request):
    filtro = []
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u'organismo_id=%s'%request.GET['organismo'])   
    if 'dependencia' in request.GET:
        if request.GET['dependencia']:
            filtro.append(u'dependencia=%s'%request.GET['dependencia'])    
    query = Twitter.objects.extra(where=filtro, select={'dependencia':"case organismo_id when 1 then (select ministerio from ministerio where nummin=dependencia) when 2 then (select odp from odp where numodp=dependencia) when 3 then (select gobernacion from gobernacion where numgob=dependencia) end",})
    html = render_to_string('redes/twitter_reporte.html',{'data': query,'pagesize':'A4','usuario':request.user.get_profile()},context_instance=RequestContext(request))
    filename= "twitter_%s.pdf" % datetime.today().strftime("%Y%m%d")        
    return imprimirToPDF(html,filename)

@login_required(login_url='/')
def twitterdiario(request):
    mensaje = ''
    if request.method == 'POST':  
        num = TwitterDiario.objects.values("numtwdia").order_by("-numtwdia",)[:1]
	num = 1 if len(num)==0 else int(num[0]["numtwdia"])+1
        profile = Usuario.objects.get(user = request.user) 
        itwittwer = TwitterDiario(numtwdia=num,idusuario_creac=profile,organismo=profile.organismo,dependencia=profile.dependencia)
        frmtwitterdiario = TwitterDiarioForm(request.POST, instance=itwittwer)
        if frmtwitterdiario.is_valid():
            frmtwitterdiario.save()
            frmtwitterdiario = TwitterDiarioForm()
            mensaje = 'Registro grabado satisfactoriamente'
    else:        
        frmtwitterdiario = TwitterDiarioForm()
    return render_to_response('redes/twitterdiario.html', {'frmtwitterdiario': frmtwitterdiario,'opcion':'add','mensaje':mensaje}, context_instance=RequestContext(request),)

@login_required()
def twitterdiario_edit(request, codigo):
    if request.method == 'POST':
        info = get_object_or_404(Informacion, numinf=int(codigo))  
        info.idusuario_mod = request.user.get_profile()
        info.fec_mod = datetime.now()
        dependencia = info.dependencia
        formulario = InformacionForm(request.POST, instance=info) # A form bound to the POST data
        if formulario.is_valid():
            formulario.save()
            return redirect(reverse('ogcs-redes-informacion-query')+'?m=edit') # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        info = get_object_or_404(Informacion, numinf=int(codigo))        
        dependencia = info.dependencia
        formulario = InformacionForm(instance=info)
    return render_to_response('redes/informacion.html', {'formulario': formulario,'opcion':'edit','codigo':codigo,'dependencia':dependencia,}, context_instance=RequestContext(request),)

@login_required()
def twitterdiario_consulta(request):
    filtro = []
    mensaje = request.GET['m'] if 'm' in request.GET else None
    dependencia= None
    #filtros
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u'organismo_id=%s'%request.GET['organismo'])   
    if 'dependencia' in request.GET:
        if request.GET['dependencia']:
            filtro.append(u'dependencia=%s'%request.GET['dependencia'])
            dependencia = request.GET['dependencia']
    formulario = TwitterDiarioConsultaForm(request.GET)
    query = TwitterDiario.objects.extra(where=filtro, select={'dependencia':"case organismo_id when 1 then (select ministerio from ministerio where nummin=dependencia) when 2 then (select odp from odp where numodp=dependencia) when 3 then (select gobernacion from gobernacion where numgob=dependencia) end"})
    tabla = TwitterDiarioTable(query)
    RequestConfig(request).configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('redes/twitterdiario_consulta.html',{'formulario':formulario,'tabla':tabla,'dependencia':dependencia,'mensaje':mensaje},context_instance=RequestContext(request))

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


