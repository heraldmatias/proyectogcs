# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from forms import InformacionForm, TwitterForm, TwitterDetalleForm, FacebookForm, FacebookDetalleForm,FacebookDiarioForm, TwitterDiarioForm,InformacionConsultaForm, InformacionTable, DetalleTwitterTable, TwitterConsultaForm, TwitterTable,TwitterDiarioConsultaForm, TwitterDiarioTable, FacebookDetalleTable, FacebookConsultaForm, FacebookTable, FacebookDiarioTable, FacebookDiarioConsultaForm, YoutubeForm, YoutubeConsultaForm, YoutubeTable, YoutubeDetalleForm, YoutubeDetalleTable, YoutubeDiarioForm, YoutubeDiarioConsultaForm, YoutubeDiarioTable, YoutubeDiarioDetalleForm, YoutubeDiarioDetalleTable
from django.template import RequestContext
from usuario.models import Usuario, Estado
from django.contrib.auth.decorators import login_required
from models import Informacion, Twitter, TwitterDetalle, Facebook, FacebookDetalle, TwitterDiario, FacebookDiario, Youtube, YoutubeDetalle, YoutubeDiario, YoutubeDiarioDetalle
from datetime import datetime
from django_tables2.config import RequestConfig
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from scripts.scripts import imprimirToPDF, DivErrorList
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
        frminformacion = InformacionForm(request.POST, instance=iinformacion,error_class=DivErrorList) # A form bound to the POST data
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
        formulario = InformacionForm(request.POST, instance=info,error_class=DivErrorList) # A form bound to the POST data
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
        frmtwitter = TwitterForm(request.POST, instance=itwittwer,error_class=DivErrorList) # A form bound to the POST data
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
        frmtwitter = TwitterForm(request.POST, instance=itwitter,error_class=DivErrorList)  
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
        frmtwitterdiario = TwitterDiarioForm(request.POST, instance=itwittwer,error_class=DivErrorList)
        if frmtwitterdiario.is_valid():
            frmtwitterdiario.save()
            frmtwitterdiario = TwitterDiarioForm()
            mensaje = 'Registro grabado satisfactoriamente'
    else:        
        frmtwitterdiario = TwitterDiarioForm()
    return render_to_response('redes/twitterdiario.html', {'formulario': frmtwitterdiario,'opcion':'add','mensaje':mensaje}, context_instance=RequestContext(request),)

@login_required()
def twitterdiario_edit(request, codigo):
    if request.method == 'POST':
        info = get_object_or_404(TwitterDiario, numtwdia=int(codigo))
        profile = Usuario.objects.get(user = request.user)   
        if profile.nivel.codigo == 1:
            info.fec_mod = datetime.now()
            info.idusuario_mod = profile
        else:
            info.idadministrador_mod = profile
            info.fec_modadm = datetime.now()  
        formulario = TwitterDiarioForm(request.POST, instance=info,error_class=DivErrorList) # A form bound to the POST data
        if formulario.is_valid():
            formulario.save()
            return redirect(reverse('ogcs-redes-twitter-diario-query')+'?m=edit') # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        info = get_object_or_404(TwitterDiario, numtwdia=int(codigo))        
        info.fechacreacdia = info.fechacreacdia.strftime("%d/%m/%Y") 
        formulario = TwitterDiarioForm(instance=info)
    return render_to_response('redes/twitterdiario.html', {'formulario': formulario,'opcion':'edit','codigo':codigo,}, context_instance=RequestContext(request),)

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
    if 'fechaini' in request.GET and 'fechafin' in request.GET:
        if request.GET['fechaini'] and request.GET['fechafin']:
            fini = datetime.strptime(request.GET['fechaini'],"%d/%m/%Y")
            ffin = datetime.strptime(request.GET['fechafin'],"%d/%m/%Y")
            filtro.append(u"fechacreacdia between '%s' and '%s'"%(fini,ffin))
        elif 'fechaini' in request.GET:
            if request.GET['fechaini']:
                fini = datetime.strptime(request.GET['fechaini'],"%d/%m/%Y")            
                filtro.append(u"fechacreacdia>='%s'"%fini)
            elif 'fechafin' in request.GET:
                if request.GET['fechafin']:
                    ffin = datetime.strptime(request.GET['fechafin'],"%d/%m/%Y")            
                    filtro.append(u"fechacreacdia<='%s'"%ffin)
    formulario = TwitterDiarioConsultaForm(request.GET) if len(request.GET) != 0 else TwitterDiarioConsultaForm()
    query = TwitterDiario.objects.extra(where=filtro, select={'dependencia':"case organismo_id when 1 then (select ministerio from ministerio where nummin=dependencia) when 2 then (select odp from odp where numodp=dependencia) when 3 then (select gobernacion from gobernacion where numgob=dependencia) end"})
    tabla = TwitterDiarioTable(query)
    RequestConfig(request).configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('redes/twitterdiario_consulta.html',{'formulario':formulario,'tabla':tabla,'dependencia':dependencia,'mensaje':mensaje},context_instance=RequestContext(request))

@login_required()
def twitterdiario_print(request):
    filtro = []
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u'organismo_id=%s'%request.GET['organismo'])   
    if 'dependencia' in request.GET:
        if request.GET['dependencia']:
            filtro.append(u'dependencia=%s'%request.GET['dependencia'])
            dependencia = request.GET['dependencia']
    if 'fechaini' in request.GET and 'fechafin' in request.GET:
        if request.GET['fechaini'] and request.GET['fechafin']:
            fini = datetime.strptime(request.GET['fechaini'],"%d/%m/%Y")
            ffin = datetime.strptime(request.GET['fechafin'],"%d/%m/%Y")
            filtro.append(u"fechacreacdia between '%s' and '%s'"%(fini,ffin))
        elif 'fechaini' in request.GET:
            if request.GET['fechaini']:
                fini = datetime.strptime(request.GET['fechaini'],"%d/%m/%Y")            
                filtro.append(u"fechacreacdia>='%s'"%fini)
            elif 'fechafin' in request.GET:
                if request.GET['fechafin']:
                    ffin = datetime.strptime(request.GET['fechafin'],"%d/%m/%Y")            
                    filtro.append(u"fechacreacdia<='%s'"%ffin)
    query = TwitterDiario.objects.extra(where=filtro, select={'dependencia':"case organismo_id when 1 then (select ministerio from ministerio where nummin=dependencia) when 2 then (select odp from odp where numodp=dependencia) when 3 then (select gobernacion from gobernacion where numgob=dependencia) end"})
    html = render_to_string('redes/twitterdiario_reporte.html',{'data': query,'pagesize':'A4','usuario':request.user.get_profile()},context_instance=RequestContext(request))
    filename= "twitterdiario_%s.pdf" % datetime.today().strftime("%Y%m%d")        
    return imprimirToPDF(html,filename)

@login_required(login_url='/')
def facebook(request): 
    mensaje = ''  
    if request.method == 'POST':  
        num = Facebook.objects.values("numfb").order_by("-numfb",)[:1]
	num = 1 if len(num)==0 else int(num[0]["numfb"])+1
        profile = Usuario.objects.get(user = request.user) 
        ifacebook = Facebook(numfb=num,idusuario_creac=profile,organismo=profile.organismo,dependencia=profile.dependencia)
        frmfacebook = FacebookForm(request.POST, instance=ifacebook,error_class=DivErrorList) # A form bound to the POST data
        if frmfacebook.is_valid():
            frmfacebook.save()
            fechas = request.POST.getlist('tfechas')
            likes = request.POST.getlist('tlikes')
	    for co in range(len(fechas)):
                fecha = fechas[co]
                fecha = datetime.strptime(fecha,"%d/%m/%Y")
                det = FacebookDetalle(numfb=ifacebook,item=co+1,fechadetfb = fecha,cantidad=likes[co],)
                det.save() 
                mensaje = 'Registro grabado satisfactoriamente'   
                frmfacebook = FacebookForm()
    else:        
        frmfacebook = FacebookForm()
    frmfacebookdetalle = FacebookDetalleForm()
    tabla = FacebookDetalleTable([])
    return render_to_response('redes/facebook.html', {'formulario': frmfacebook,'frm_detalle':frmfacebookdetalle,'opcion':'add','tabla':tabla,'mensaje':mensaje}, context_instance=RequestContext(request),)

@login_required()
def facebook_edit(request, codigo): 
    mensaje = ''
    if request.method == 'POST':  
        obj = get_object_or_404(Facebook,pk=codigo)
        profile = request.user.get_profile()
        if profile.nivel.codigo == 1:
            obj.fec_mod = datetime.now()
            obj.idusuario_mod = profile
        else:
            obj.idadministrador_mod = profile
            obj.fec_modadm = datetime.now()      
        formulario = FacebookForm(request.POST, instance=obj,error_class=DivErrorList)  
        if formulario.is_valid():
            formulario.save()
            fechas = request.POST.getlist('tfechas')
            likes = request.POST.getlist('tlikes')            
	    #FACEBOOK_DETALLE_save
            query = FacebookDetalle.objects.filter(numfb=obj)
            for c in range(len(likes)):
                fecha = datetime.strptime(fechas[c],"%d/%m/%Y")
                try:
                    row = FacebookDetalle.objects.get(numfb=obj,item=c+1)
                    row.fechadetfb = fecha
                    row.cantidad = likes[c]
                    row.save()
                except FacebookDetalle.DoesNotExist:
                    FacebookDetalle(numfb=obj,item=c+1,fechadetfb = fecha,cantidad=likes[c],).save()
            resto= len(likes)
            while resto < len(query):
                row = FacebookDetalle.objects.get(numfb=obj,item=resto+1)
                row.delete()
                resto = resto + 1
            return redirect(reverse('ogcs-redes-facebook-query')+'?m=edit') 
    else: 
        obj = get_object_or_404(Facebook,pk=codigo)
        obj.fechacreac = obj.fechacreac.strftime("%d/%m/%Y")       
        formulario = FacebookForm(instance = obj)
    detalle = FacebookDetalle.objects.filter(numfb=obj)#.order_by('-fechadettw')
    for row in detalle:
        row.fechadetfb = row.fechadetfb.strftime("%d/%m/%Y")
    tabla = FacebookDetalleTable(detalle)
    frm_detalle = FacebookDetalleForm()
    return render_to_response('redes/facebook.html', {'formulario': formulario,'frm_detalle':frm_detalle,'opcion':'edit','codigo':codigo,'tabla':tabla}, context_instance=RequestContext(request),)

@login_required()
def facebook_consulta(request):
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
    formulario = FacebookConsultaForm(request.GET)
    query = Facebook.objects.extra(where=filtro, select={'dependencia':"case organismo_id when 1 then (select ministerio from ministerio where nummin=dependencia) when 2 then (select odp from odp where numodp=dependencia) when 3 then (select gobernacion from gobernacion where numgob=dependencia) end"})
    tabla = FacebookTable(query)
    RequestConfig(request).configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('redes/facebook_consulta.html',{'formulario':formulario,'tabla':tabla,'dependencia':dependencia,'mensaje':mensaje},context_instance=RequestContext(request))

@login_required()
def facebook_print(request):
    filtro = []
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u'organismo_id=%s'%request.GET['organismo'])   
    if 'dependencia' in request.GET:
        if request.GET['dependencia']:
            filtro.append(u'dependencia=%s'%request.GET['dependencia'])    
    query = Facebook.objects.extra(where=filtro, select={'dependencia':"case organismo_id when 1 then (select ministerio from ministerio where nummin=dependencia) when 2 then (select odp from odp where numodp=dependencia) when 3 then (select gobernacion from gobernacion where numgob=dependencia) end",})
    html = render_to_string('redes/facebook_reporte.html',{'data': query,'pagesize':'A4','usuario':request.user.get_profile()},context_instance=RequestContext(request))
    filename= "facebook_%s.pdf" % datetime.today().strftime("%Y%m%d")        
    return imprimirToPDF(html,filename)

@login_required(login_url='/')
def facebookdiario(request):   
    mensaje = ''
    if request.method == 'POST':  
        num = FacebookDiario.objects.values("numfbdia").order_by("-numfbdia",)[:1]
	num = 1 if len(num)==0 else int(num[0]["numfbdia"])+1
        profile = Usuario.objects.get(user = request.user) 
        obj = FacebookDiario(numfbdia=num,idusuario_creac=profile,organismo=profile.organismo,dependencia=profile.dependencia)
        frmfacebookdiario = FacebookDiarioForm(request.POST, instance=obj,error_class=DivErrorList) # A form bound to the POST data
        if frmfacebookdiario.is_valid():
            frmfacebookdiario.save()
            mensaje= 'Registro grabado satisfactoriamente'
            frmfacebookdiario = FacebookDiarioForm()
    else:        
        frmfacebookdiario = FacebookDiarioForm()
    return render_to_response('redes/facebookdiario.html', {'formulario': frmfacebookdiario,'opcion':'add','mensaje':mensaje}, context_instance=RequestContext(request),)


@login_required()
def facebookdiario_edit(request, codigo):
    if request.method == 'POST':
        info = get_object_or_404(FacebookDiario, numfbdia=int(codigo))
        profile = Usuario.objects.get(user = request.user)   
        if profile.nivel.codigo == 1:
            info.fec_mod = datetime.now()
            info.idusuario_mod = profile
        else:
            info.idadministrador_mod = profile
            info.fec_modadm = datetime.now()  
        formulario = FacebookDiarioForm(request.POST, instance=info,error_class=DivErrorList) # A form bound to the POST data
        if formulario.is_valid():
            formulario.save()
            return redirect(reverse('ogcs-redes-facebook-diario-query')+'?m=edit') # Crear un parametro en home para mostrar los mensajes de exito.
    else:        
        info = get_object_or_404(FacebookDiario, numfbdia=int(codigo))        
        info.fechacreacdia = info.fechacreacdia.strftime("%d/%m/%Y") 
        formulario = FacebookDiarioForm(instance=info)
    return render_to_response('redes/facebookdiario.html', {'formulario': formulario,'opcion':'edit','codigo':codigo,}, context_instance=RequestContext(request),)

@login_required()
def facebookdiario_consulta(request):
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
    if 'fechaini' in request.GET and 'fechafin' in request.GET:
        if request.GET['fechaini'] and request.GET['fechafin']:
            fini = datetime.strptime(request.GET['fechaini'],"%d/%m/%Y")
            ffin = datetime.strptime(request.GET['fechafin'],"%d/%m/%Y")
            filtro.append(u"fechacreacdia between '%s' and '%s'"%(fini,ffin))
        elif 'fechaini' in request.GET:
            if request.GET['fechaini']:
                fini = datetime.strptime(request.GET['fechaini'],"%d/%m/%Y")            
                filtro.append(u"fechacreacdia>='%s'"%fini)
            elif 'fechafin' in request.GET:
                if request.GET['fechafin']:
                    ffin = datetime.strptime(request.GET['fechafin'],"%d/%m/%Y")            
                    filtro.append(u"fechacreacdia<='%s'"%ffin)
    formulario = FacebookDiarioConsultaForm(request.GET) if len(request.GET) != 0 else FacebookDiarioConsultaForm()
    query = FacebookDiario.objects.extra(where=filtro, select={'dependencia':"case organismo_id when 1 then (select ministerio from ministerio where nummin=dependencia) when 2 then (select odp from odp where numodp=dependencia) when 3 then (select gobernacion from gobernacion where numgob=dependencia) end"})
    tabla = FacebookDiarioTable(query)
    RequestConfig(request).configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('redes/facebookdiario_consulta.html',{'formulario':formulario,'tabla':tabla,'dependencia':dependencia,'mensaje':mensaje},context_instance=RequestContext(request))

@login_required()
def facebookdiario_print(request):
    filtro = []
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u'organismo_id=%s'%request.GET['organismo'])   
    if 'dependencia' in request.GET:
        if request.GET['dependencia']:
            filtro.append(u'dependencia=%s'%request.GET['dependencia'])
            dependencia = request.GET['dependencia']
    if 'fechaini' in request.GET and 'fechafin' in request.GET:
        if request.GET['fechaini'] and request.GET['fechafin']:
            fini = datetime.strptime(request.GET['fechaini'],"%d/%m/%Y")
            ffin = datetime.strptime(request.GET['fechafin'],"%d/%m/%Y")
            filtro.append(u"fechacreacdia between '%s' and '%s'"%(fini,ffin))
        elif 'fechaini' in request.GET:
            if request.GET['fechaini']:
                fini = datetime.strptime(request.GET['fechaini'],"%d/%m/%Y")            
                filtro.append(u"fechacreacdia>='%s'"%fini)
            elif 'fechafin' in request.GET:
                if request.GET['fechafin']:
                    ffin = datetime.strptime(request.GET['fechafin'],"%d/%m/%Y")            
                    filtro.append(u"fechacreacdia<='%s'"%ffin)
    query = FacebookDiario.objects.extra(where=filtro, select={'dependencia':"case organismo_id when 1 then (select ministerio from ministerio where nummin=dependencia) when 2 then (select odp from odp where numodp=dependencia) when 3 then (select gobernacion from gobernacion where numgob=dependencia) end"})
    html = render_to_string('redes/facebookdiario_reporte.html',{'data': query,'pagesize':'A4','usuario':request.user.get_profile()},context_instance=RequestContext(request))
    filename= "facebookdiario_%s.pdf" % datetime.today().strftime("%Y%m%d")        
    return imprimirToPDF(html,filename)

@login_required(login_url='/')
def youtube(request): 
    mensaje = ''
    if request.method == 'POST':  
        num = Youtube.objects.values("numyt").order_by("-numyt",)[:1]
	num = 1 if len(num)==0 else int(num[0]["numyt"])+1
        profile = request.user.get_profile()
        obj = Youtube(numyt=num,idusuario_creac=profile,organismo=profile.organismo,dependencia=profile.dependencia)
        frm = YoutubeForm(request.POST, instance=obj,error_class=DivErrorList) # A form bound to the POST data
        if frm.is_valid():
            frm.save() #cfechas csuscrip crepro cmegusta cnomegusta ccomen ccompar cfavo cfavodel    
            fechas = request.POST.getlist('cfechas')
            suscriptores = request.POST.getlist('csuscrip')
            reproducciones = request.POST.getlist('crepro')
            megusta = request.POST.getlist('cmegusta')
            nomegusta = request.POST.getlist('cnomegusta')
            comentarios = request.POST.getlist('ccomen')
            compartidos = request.POST.getlist('ccompar')
            favoritos = request.POST.getlist('cfavo')
            favoritosdel = request.POST.getlist('cfavodel')
	    for co in range(len(fechas)):
                fecha = fechas[co]                
                fecha = datetime.strptime(fecha,"%d/%m/%Y")
                det = YoutubeDetalle(numyt=obj,item=co+1,fechadetyt = fecha,suscriptores=suscriptores[co],reproducciones =reproducciones[co], megusta = megusta[co],nomegusta=nomegusta[co],comentarios=comentarios[co],compartidos=compartidos[co],favoritos=favoritos[co],favoritosdel=favoritosdel[co],)
                det.save() 
            mensaje = 'Registro grabado satisfactoriamente'
            frm = YoutubeForm()
    else:        
        frm = YoutubeForm()
    frm_detalle = YoutubeDetalleForm()
    tabla = YoutubeDetalleTable([])
    return render_to_response('redes/youtube.html', {'formulario': frm,'frm_detalle':frm_detalle,'opcion':'add','tabla':tabla,'mensaje':mensaje}, context_instance=RequestContext(request),)

@login_required(login_url='/')
def youtube_edit(request, codigo): 
    mensaje = ''
    if request.method == 'POST':  
        obj = get_object_or_404(Youtube,pk=codigo)
        profile = request.user.get_profile()
        if profile.nivel.codigo == 1:
            obj.fec_mod = datetime.now()
            obj.idusuario_mod = profile
        else:
            obj.idadministrador_mod = profile
            obj.fec_modadm = datetime.now()      
        frm = YoutubeForm(request.POST, instance=obj,error_class=DivErrorList)  
        if frm.is_valid():
            frm.save()
            fechas = request.POST.getlist('cfechas')
            suscriptores = request.POST.getlist('csuscrip')
            reproducciones = request.POST.getlist('crepro')
            megusta = request.POST.getlist('cmegusta')
            nomegusta = request.POST.getlist('cnomegusta')
            comentarios = request.POST.getlist('ccomen')
            compartidos = request.POST.getlist('ccompar')
            favoritos = request.POST.getlist('cfavo')
            favoritosdel = request.POST.getlist('cfavodel')
	    #TWITTER_DETALLE_save
            query = YoutubeDetalle.objects.filter(numyt=obj)
            for co in range(len(fechas)):
                fecha = datetime.strptime(fechas[co],"%d/%m/%Y")
                try:
                    row = YoutubeDetalle.objects.get(numyt=obj,item=co+1)
                    row.fechadetyt = fecha
                    row.suscriptores = suscriptores[co]
                    row.reproducciones = reproducciones[co]
                    row.megusta = megusta[co]
                    row.nomegusta = nomegusta[co]
                    row.comentarios = comentarios[co]
                    row.compartidos = compartidos[co]
                    row.favoritos = favoritos[co]
                    row.favoritosdel = favoritosdel[co]
                    row.save()
                except YoutubeDetalle.DoesNotExist:
                    YoutubeDetalle(numyt=obj,item=co+1,fechadetyt = fecha,suscriptores=suscriptores[co],reproducciones =reproducciones[co], megusta = megusta[co],nomegusta=nomegusta[co],comentarios=comentarios[co],compartidos=compartidos[co],favoritos=favoritos[co],favoritosdel=favoritosdel[co],).save()
            resto= len(fechas)
            while resto < len(query):
                row = YoutubeDetalle.objects.get(numyt=obj,item=resto+1)
                row.delete()
                resto = resto + 1
            return redirect(reverse('ogcs-redes-youtube-query')+'?m=edit') 
    else: 
        obj = get_object_or_404(Youtube,pk=codigo)
        obj.fechacreac = obj.fechacreac.strftime("%d/%m/%Y")       
        frm = YoutubeForm(instance = obj)
    detalle = YoutubeDetalle.objects.filter(numyt=obj)#.order_by('-fechadettw')
    for row in detalle:
        row.fechadetyt = row.fechadetyt.strftime("%d/%m/%Y")
    tabla = YoutubeDetalleTable(detalle)
    frm_detalle = YoutubeDetalleForm()
    return render_to_response('redes/youtube.html', {'formulario': frm,'frm_detalle':frm_detalle,'opcion':'edit','codigo':codigo,'tabla':tabla}, context_instance=RequestContext(request),)

@login_required()
def youtube_consulta(request):
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
    query = Youtube.objects.extra(where=filtro, select={'dependencia':"case organismo_id when 1 then (select ministerio from ministerio where nummin=dependencia) when 2 then (select odp from odp where numodp=dependencia) when 3 then (select gobernacion from gobernacion where numgob=dependencia) end"})
    tabla = YoutubeTable(query)
    RequestConfig(request).configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('redes/youtube_consulta.html',{'formulario':formulario,'tabla':tabla,'dependencia':dependencia,'mensaje':mensaje},context_instance=RequestContext(request))

@login_required()
def youtube_print(request):
    filtro = []
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u'organismo_id=%s'%request.GET['organismo'])   
    if 'dependencia' in request.GET:
        if request.GET['dependencia']:
            filtro.append(u'dependencia=%s'%request.GET['dependencia'])    
    query = Youtube.objects.extra(where=filtro, select={'dependencia':"case organismo_id when 1 then (select ministerio from ministerio where nummin=dependencia) when 2 then (select odp from odp where numodp=dependencia) when 3 then (select gobernacion from gobernacion where numgob=dependencia) end",})
    html = render_to_string('redes/youtube_reporte.html',{'data': query,'pagesize':'A4','usuario':request.user.get_profile()},context_instance=RequestContext(request))
    filename= "youtube_%s.pdf" % datetime.today().strftime("%Y%m%d")        
    return imprimirToPDF(html,filename)

@login_required()
def youtubediario(request): 
    mensaje = ''
    if request.method == 'POST':  
        num = YoutubeDiario.objects.values("numytdia").order_by("-numytdia",)[:1]
	num = 1 if len(num)==0 else int(num[0]["numytdia"])+1
        profile = request.user.get_profile()
        obj = YoutubeDiario(numytdia=num,idusuario_creac=profile,organismo=profile.organismo,dependencia=profile.dependencia)
        frm = YoutubeDiarioForm(request.POST, instance=obj,error_class=DivErrorList) # A form bound to the POST data
        if frm.is_valid():
            frm.save() #cfechas csuscrip crepro cmegusta cnomegusta ccomen ccompar cfavo cfavodel    
            fechas = request.POST.getlist('cfechas')
            titulo = request.POST.getlist('ctitulo')
            urlytdia = request.POST.getlist('curl')
            suscriptores = request.POST.getlist('csuscrip')
            reproducciones = request.POST.getlist('crepro')
            megusta = request.POST.getlist('cmegusta')
            nomegusta = request.POST.getlist('cnomegusta')
            comentarios = request.POST.getlist('ccomen')
            compartidos = request.POST.getlist('ccompar')
            favoritos = request.POST.getlist('cfavo')
            favoritosdel = request.POST.getlist('cfavodel')
	    for co in range(len(fechas)):
                fecha = fechas[co]                
                fecha = datetime.strptime(fecha,"%d/%m/%Y")
                det = YoutubeDiarioDetalle(numytdia=obj,item=co+1,fechadetytdia = fecha,titulo=titulo[co],urlytdia=urlytdia[co],suscriptores=suscriptores[co],reproducciones =reproducciones[co], megusta = megusta[co],nomegusta=nomegusta[co],comentarios=comentarios[co],compartidos=compartidos[co],favoritos=favoritos[co],favoritosdel=favoritosdel[co],)
                det.save() 
            mensaje = 'Registro grabado satisfactoriamente'
            frm = YoutubeDiarioForm()
    else:        
        frm = YoutubeDiarioForm()
    frm_detalle = YoutubeDiarioDetalleForm()
    tabla = YoutubeDiarioDetalleTable([])
    return render_to_response('redes/youtubediario.html', {'formulario': frm,'frm_detalle':frm_detalle,'opcion':'add','tabla':tabla,'mensaje':mensaje}, context_instance=RequestContext(request),)

@login_required()
def youtubediario_edit(request, codigo): 
    mensaje = ''
    if request.method == 'POST':  
        obj = get_object_or_404(YoutubeDiario,pk=codigo)
        profile = request.user.get_profile()
        if profile.nivel.codigo == 1:
            obj.fec_mod = datetime.now()
            obj.idusuario_mod = profile
        else:
            obj.idadministrador_mod = profile
            obj.fec_modadm = datetime.now()      
        frm = YoutubeDiarioForm(request.POST, instance=obj,error_class=DivErrorList)  
        if frm.is_valid():
            frm.save()
            fechas = request.POST.getlist('cfechas')
            titulo = request.POST.getlist('ctitulo')
            urlytdia = request.POST.getlist('curl')
            suscriptores = request.POST.getlist('csuscrip')
            reproducciones = request.POST.getlist('crepro')
            megusta = request.POST.getlist('cmegusta')
            nomegusta = request.POST.getlist('cnomegusta')
            comentarios = request.POST.getlist('ccomen')
            compartidos = request.POST.getlist('ccompar')
            favoritos = request.POST.getlist('cfavo')
            favoritosdel = request.POST.getlist('cfavodel')
	    #TWITTER_DETALLE_save
            query = YoutubeDiarioDetalle.objects.filter(numytdia=obj)
            for co in range(len(fechas)):
                fecha = datetime.strptime(fechas[co],"%d/%m/%Y")
                try:
                    row = YoutubeDiarioDetalle.objects.get(numytdia=obj,item=co+1)
                    row.fechadetytdia = fecha
                    row.titulo = titulo[co]
                    row.urlytdia = urlytdia[co] 
                    row.suscriptores = suscriptores[co]
                    row.reproducciones = reproducciones[co]
                    row.megusta = megusta[co]
                    row.nomegusta = nomegusta[co]
                    row.comentarios = comentarios[co]
                    row.compartidos = compartidos[co]
                    row.favoritos = favoritos[co]
                    row.favoritosdel = favoritosdel[co]
                    row.save()
                except YoutubeDiarioDetalle.DoesNotExist:
                    YoutubeDiarioDetalle(numytdia=obj,item=co+1,fechadetytdia = fecha,titulo=titulo[co],urlytdia=urlytdia[co],suscriptores=suscriptores[co],reproducciones =reproducciones[co], megusta = megusta[co],nomegusta=nomegusta[co],comentarios=comentarios[co],compartidos=compartidos[co],favoritos=favoritos[co],favoritosdel=favoritosdel[co],).save()
            resto= len(fechas)
            while resto < len(query):
                row = YoutubeDiarioDetalle.objects.get(numytdia=obj,item=resto+1)
                row.delete()
                resto = resto + 1
            return redirect(reverse('ogcs-redes-youtube-diario-query')+'?m=edit') 
    else: 
        obj = get_object_or_404(YoutubeDiario,pk=codigo)
        obj.fechacreacdia = obj.fechacreacdia.strftime("%d/%m/%Y")       
        frm = YoutubeDiarioForm(instance = obj)
    detalle = YoutubeDiarioDetalle.objects.filter(numytdia=obj)#.order_by('-fechadettw')
    for row in detalle:
        row.fechadetytdia = row.fechadetytdia.strftime("%d/%m/%Y")
    tabla = YoutubeDiarioDetalleTable(detalle)
    frm_detalle = YoutubeDiarioDetalleForm()
    return render_to_response('redes/youtubediario.html', {'formulario': frm,'frm_detalle':frm_detalle,'opcion':'edit','codigo':codigo,'tabla':tabla}, context_instance=RequestContext(request),)

@login_required()
def youtubediario_consulta(request):
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
    if 'fechaini' in request.GET and 'fechafin' in request.GET:
        if request.GET['fechaini'] and request.GET['fechafin']:
            fini = datetime.strptime(request.GET['fechaini'],"%d/%m/%Y")
            ffin = datetime.strptime(request.GET['fechafin'],"%d/%m/%Y")
            filtro.append(u"fechacreacdia between '%s' and '%s'"%(fini,ffin))
        elif 'fechaini' in request.GET:
            if request.GET['fechaini']:
                fini = datetime.strptime(request.GET['fechaini'],"%d/%m/%Y")            
                filtro.append(u"fechacreacdia>='%s'"%fini)
            elif 'fechafin' in request.GET:
                if request.GET['fechafin']:
                    ffin = datetime.strptime(request.GET['fechafin'],"%d/%m/%Y")            
                    filtro.append(u"fechacreacdia<='%s'"%ffin)
    formulario = YoutubeDiarioConsultaForm(request.GET)
    query = YoutubeDiario.objects.extra(where=filtro, select={'dependencia':"case organismo_id when 1 then (select ministerio from ministerio where nummin=dependencia) when 2 then (select odp from odp where numodp=dependencia) when 3 then (select gobernacion from gobernacion where numgob=dependencia) end"})
    tabla = YoutubeDiarioTable(query)
    RequestConfig(request).configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('redes/youtubediario_consulta.html',{'formulario':formulario,'tabla':tabla,'dependencia':dependencia,'mensaje':mensaje},context_instance=RequestContext(request))

@login_required()
def youtubediario_print(request):
    filtro = []
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u'organismo_id=%s'%request.GET['organismo'])   
    if 'dependencia' in request.GET:
        if request.GET['dependencia']:
            filtro.append(u'dependencia=%s'%request.GET['dependencia'])  
    if 'fechaini' in request.GET and 'fechafin' in request.GET:
        if request.GET['fechaini'] and request.GET['fechafin']:
            fini = datetime.strptime(request.GET['fechaini'],"%d/%m/%Y")
            ffin = datetime.strptime(request.GET['fechafin'],"%d/%m/%Y")
            filtro.append(u"fechacreacdia between '%s' and '%s'"%(fini,ffin))
        elif 'fechaini' in request.GET:
            if request.GET['fechaini']:
                fini = datetime.strptime(request.GET['fechaini'],"%d/%m/%Y")            
                filtro.append(u"fechacreacdia>='%s'"%fini)
            elif 'fechafin' in request.GET:
                if request.GET['fechafin']:
                    ffin = datetime.strptime(request.GET['fechafin'],"%d/%m/%Y")            
                    filtro.append(u"fechacreacdia<='%s'"%ffin)  
    query = YoutubeDiario.objects.extra(where=filtro, select={'dependencia':"case organismo_id when 1 then (select ministerio from ministerio where nummin=dependencia) when 2 then (select odp from odp where numodp=dependencia) when 3 then (select gobernacion from gobernacion where numgob=dependencia) end",})
    html = render_to_string('redes/youtubediario_reporte.html',{'data': query,'pagesize':'A4','usuario':request.user.get_profile()},context_instance=RequestContext(request))
    filename= "youtubediario_%s.pdf" % datetime.today().strftime("%Y%m%d")        
    return imprimirToPDF(html,filename)


