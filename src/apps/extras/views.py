# -*- coding: utf-8 -*-
from forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from models import Documento
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import get_object_or_404
import django_tables2 as tables
from django_tables2.config import RequestConfig
from datetime import datetime
from scripts.scripts import imprimirToPDF, DivErrorList
from django.http import HttpResponse, Http404
from django.core.files.storage import  FileSystemStorage,default_storage
from usuario.models import Usuario
from django.template.loader import render_to_string
from pybb.models import Category, Topic, Forum
from django.core.urlresolvers import reverse

@login_required()
def view_calendar(request):
    return render_to_response('extras/calendario.html', context_instance=RequestContext(request),)

def get_categoria(tipo):
   """
      Define la categoria del documento subido, VER campo estatico CATEGORIAS en models.py
   """
   categoria = 'OTROS'
   if tipo in ('JPG','GIF','ICO','PNG','TIF',):   
       categoria = 'IMAGENES'
   elif tipo in ('AVI','MOV','MP4','WMV','FLV','F4V','3GP'):   
       categoria = 'VIDEOS' 
   elif tipo in ('MP3','WAV','AMF','AMV','OGG'):
       categoria = 'AUDIOS'
   elif tipo in ('DOC','DOCX','PDF','PPT','PPTX','XLS','XLSX','TXT','ODT'):
       categoria = 'DOCUMENTOS'
   elif tipo in ('ZIP','TAR','GZ','ZIP','RAR','7Z',):
       categoria = 'COMPRIMIDOS'
   return categoria

@login_required()
def documentos_add(request):
    mensaje = ''
    if request.method == 'POST':
        if 'archivo' in request.FILES:
            profile = request.user.get_profile()
            ini=profile.get_dependencia()            
            archivo = request.FILES['archivo']
            extension = archivo.name[archivo.name.rfind('.')+1:].upper()
            cat = get_categoria(extension)
            filename= "%s%s.%s" % (ini.iniciales,datetime.today().strftime("%d%m%Y%S"),extension)
            request.FILES['archivo'].name = filename
            obj = Documento(organismo=profile.organismo, dependencia=profile.dependencia,tipo= cat == 'OTROS' and 'OTRO' or extension,categoria=cat,idusuario_creac=profile)
            formulario = DocumentoForm(request.POST,request.FILES,instance=obj ) # A form bound to the POST data
            if formulario.is_valid():
                formulario.save()             
                obj.url_archivo=obj.archivo.url 
                obj.save()
                mensaje="Registro grabado satisfactoriamente."
        formulario = DocumentoForm()
    else:        
        formulario = DocumentoForm()
    return render_to_response('extras/documento.html', {'formulario': formulario,'mensaje':mensaje,}, context_instance=RequestContext(request),)

@login_required()
def documentos_query(request):
    col = "-organismo"
    query = None
    dependencia=''
    usuario = ''
    filtro = list()
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    formulario = ConsultaDocumentoForm(request.GET)
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u"documentos.organismo_id =%s"%request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"documentos.dependencia =%s"%request.GET['dependencia'])
                dependencia=request.GET['dependencia']
    if 'idusuario_creac' in request.GET:
        if request.GET['idusuario_creac']:
            filtro.append(u"idusuario_creac_id =%s"%request.GET['idusuario_creac'])
            usuario=request.GET['idusuario_creac']
    if 'categoria' in request.GET:
        if request.GET['categoria']:
            filtro.append(u"categoria ='%s'"%request.GET['categoria'])
    if 'tipo' in request.GET:
        if request.GET['tipo']:
            filtro.append(u"tipo ='%s'"%request.GET['tipo'])   
    query = Documento.objects.extra(where=filtro,select={'dependencia':"case documentos.organismo_id when 1 then (select ministerio from ministerio where nummin=documentos.dependencia) when 2 then (select odp from odp where numodp=documentos.dependencia) when 3 then (select gobernacion from gobernacion where numgob=documentos.dependencia) end"})
#.filter(nombreari__icontains=request.GET['nombreari'] if 'nombreari' in request.GET else '')
    tabla = DocumentoTable(query.order_by(col))
    config.configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('extras/documento_consulta.html', {'formulario': formulario,'tabla':tabla,'dependencia':dependencia,'usuario':usuario}, context_instance=RequestContext(request),)

@login_required()
def documentos_print(request):
    col = "-organismo"
    query = None
    dependencia=''
    usuario = ''
    filtro = list()
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    formulario = ConsultaDocumentoForm(request.GET)
    if 'organismo' in request.GET:
        if request.GET['organismo']:
            filtro.append(u"documentos.organismo_id =%s"%request.GET['organismo'])
        if 'dependencia' in request.GET:
            if request.GET['dependencia']:
                filtro.append(u"documentos.dependencia =%s"%request.GET['dependencia'])
                dependencia=request.GET['dependencia']
    if 'idusuario_creac' in request.GET:
        if request.GET['idusuario_creac']:
            filtro.append(u"idusuario_creac_id =%s"%request.GET['idusuario_creac'])
            usuario=request.GET['idusuario_creac']
    if 'categoria' in request.GET:
        if request.GET['categoria']:
            filtro.append(u"categoria ='%s'"%request.GET['categoria'])
    if 'tipo' in request.GET:
        if request.GET['tipo']:
            filtro.append(u"tipo ='%s'"%request.GET['tipo'])
    query = Documento.objects.extra(where=filtro,select={'dependencia':"case documentos.organismo_id when 1 then (select ministerio from ministerio where nummin=documentos.dependencia) when 2 then (select odp from odp where numodp=documentos.dependencia) when 3 then (select gobernacion from gobernacion where numgob=documentos.dependencia) end"})
    html = render_to_string('extras/reporte_doc.html',{'data': query,'pagesize':'A4','usuario':request.user.get_profile()},context_instance=RequestContext(request))
    filename= "doc_%s.pdf" % datetime.today().strftime("%Y%m%d")        
    return imprimirToPDF(html,filename)

def descargar(request,archivoo):    
    try:
        archivo = default_storage.open(archivoo)
    except:
        raise Http404
    reporte = HttpResponse(content_type='application/octet-stream')
    reporte['Content-Disposition'] = 'attachment; filename="%s"'%archivo.name[archivo.name.rfind('/')+1:]
    reporte['Content-Length'] = default_storage.size(archivo.name)
    reporte.write(archivo.read())
    return reporte

################################################################################
################################################################################
@login_required()
def forum_add(request):
    mensaje=""
    if request.method == 'POST':
        cat = Forum(idusuario_creac=request.user)
        formulario = ForummForm(request.POST,instance=cat,error_class=DivErrorList)
        if formulario.is_valid():
            formulario.save()
            #temas = request.POST.getlist('ctema')
            #cest = request.POST.getlist('cest')
            #for c in range(len(temas)):
            #    Topic(estado=cest[c],name=temas[c],forum=cat,idusuario_creac=request.user,user=request.user,created=datetime.now(),updated=datetime.now()).save()
            formulario = ForummForm() # Crear un parametro en home para mostrar los mensajes de exito.
            mensaje="Registro grabado satisfactoriamente."
    else:
        formulario = ForummForm()
    #tabla = TopicTable(list())
    return render_to_response('extras/foro.html', {'formulario': formulario,'opcion':'add','mensaje':mensaje,}, context_instance=RequestContext(request),)

login_required()
def forum_edit(request, codigo):
    if request.method == 'POST':
        cat = get_object_or_404(Forum, pk=int(codigo))
        cat.idusuario_mod=request.user
        cat.fec_mod = datetime.now()
        formulario = ForummForm(request.POST,instance=cat,error_class=DivErrorList)
        if formulario.is_valid():
            formulario.save()
            return redirect(reverse('ogcs-mantenimiento-foro-query')+'?m=edit')
    else:
        obj = get_object_or_404(Forum, pk=int(codigo))
        formulario = ForummForm(instance=obj)
        return render_to_response('extras/foro.html', {'formulario': formulario,'opcion':'edit','codigo':codigo,}, context_instance=RequestContext(request),)

@login_required()
def forum_query(request):
    col = "-name"
    query = Forum.objects.all()
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    formulario = ForumConsultaForm(request.GET)
    if "name" in request.GET:
        query = Forum.objects.filter(name__icontains=request.GET['name']).order_by(col)
    if "category" in request.GET:
        if request.GET['category']:
            query = query.filter(category__id=request.GET['category'] )
    tabla = ForumTablee(query.order_by(col))
    config.configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('extras/foro_consulta.html', {'formulario':formulario,'tabla':tabla,'mensaje':(request.GET['m'] if 'm' in request.GET else '')}, context_instance=RequestContext(request),)

@login_required()
def tema_add(request):
    mensaje=""
    if request.method == 'POST':
        cat = Topic(idusuario_creac=request.user,user=request.user,created=datetime.now(),updated=datetime.now())
        formulario = TopicForm(request.POST,instance=cat,error_class=DivErrorList)
        if formulario.is_valid():
            formulario.save()
            cat.forum.topic_count = cat.forum.topics.count()
            cat.forum.save()
            formulario = TopicForm() # Crear un parametro en home para mostrar los mensajes de exito.
            mensaje="Registro grabado satisfactoriamente."
    else:
        formulario = TopicForm()
    return render_to_response('extras/tema.html', {'formulario': formulario,'opcion':'add','mensaje':mensaje,}, context_instance=RequestContext(request),)

@login_required()
def tema_edit(request,codigo):
    mensaje=""
    if request.method == 'POST':
        cat = get_object_or_404(Topic, pk=int(codigo))
        cat.idusuario_mod=request.user
        cat.updated=datetime.now()
        cat.fec_mod=datetime.now()
        formulario = TopicForm(request.POST,instance=cat,error_class=DivErrorList)
        if formulario.is_valid():
            formulario.save()
            formulario = TopicForm() # Crear un parametro en home para mostrar los mensajes de exito.
            return redirect(reverse('ogcs-mantenimiento-tema-query')+'?m=edit')
    else:
        obj = get_object_or_404(Topic, pk=int(codigo))
        cate = obj.forum.category.id
        foru = obj.forum.id
        estado = obj.estado           
        formulario = TopicForm(instance=obj)         
    return render_to_response('extras/tema.html', {'formulario': formulario,'opcion':'edit','codigo':codigo,'cate':cate,'foru':foru,'estado':estado}, context_instance=RequestContext(request),)


login_required()
def tema_query(request):
    col = "-name"
    query = Topic.objects.all()
    idforum = ''
    if "2-sort" in request.GET:
        col = request.GET['2-sort']
    config = RequestConfig(request)
    formulario = TopicConsultaForm(request.GET)
    if "name" in request.GET:
        query = query.filter(name__icontains=request.GET['name']).order_by(col)
    if "forum" in request.GET:
        if request.GET['forum']:
            query = query.filter(forum__id=request.GET['forum'])
            idforum  = request.GET['forum']
    if "categoria" in request.GET:
        if request.GET['categoria']:
            query = query.filter(forum__category__id=request.GET['categoria'])
    tabla = TopicTablee(query.order_by(col))
    config.configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('extras/tema_consulta.html', {'formulario':formulario,'tabla':tabla,'mensaje':(request.GET['m'] if 'm' in request.GET else ''),'idforum':idforum}, context_instance=RequestContext(request),)



@login_required()
def categoria_add(request):
    mensaje=""        
    if request.method == 'POST':
        cat = Category(idusuario_creac=request.user)
        formulario = CategoryForm(request.POST, instance=cat,error_class=DivErrorList)
        if formulario.is_valid():
            formulario.save()
        #cat = Category(idusuario_creac=request.user,name=request.POST.getlist('name')[0],position=request.POST.getlist('position')[0],hidden=True if 'hidden' in request.POST else False,estado=request.POST.getlist('estado')[0])
        #cat.save()
        #foros = request.POST.getlist('cforo')
        #cpos = request.POST.getlist('cpos')
        #chid = request.POST.getlist('chid')
        #cest = request.POST.getlist('cest')
        #for c in range(len(foros)):
        #    Forum(name=foros[c],position=cpos[c],hidden= True if chid[c]=='1' else False,category=cat,idusuario_creac=request.user,estado=cest[c]).save()
            formulario = CategoryForm() # Crear un parametro en home para mostrar los mensajes de exito.
            mensaje="Registro grabado satisfactoriamente."
    else:
        formulario = CategoryForm()
    #tabla = ForumTable(list())
    #forum_form = ForumForm()
    return render_to_response('extras/categoria.html', {'formulario': formulario,'opcion':'add','mensaje':mensaje,}, context_instance=RequestContext(request),)

@login_required()
def categoria_edit(request, codigo):
    if request.method == 'POST':
        cat = get_object_or_404(Category, pk=int(codigo))
        cat.idusuario_mod=request.user
        #cat.name=request.POST['name']
        #cat.position=request.POST['position']
        #cat.hidden=True if 'hidden' in request.POST else False
        cat.fec_mod = datetime.now()
        #cat.estado=request.POST['estado']
        #cat.save()
        #foros = request.POST.getlist('cforo')
        #cpos = request.POST.getlist('cpos')
        #chid = request.POST.getlist('chid')
        #cest = request.POST.getlist('cest')
        formulario = CategoryForm(request.POST,instance=cat,error_class=DivErrorList)
        if formulario.is_valid():
            formulario.save()
            return redirect(reverse('ogcs-mantenimiento-categoria-query')+'?m=edit')
    else:
        obj = get_object_or_404(Category, pk=int(codigo))
        formulario = CategoryForm(instance=obj)
        #foros = obj.forums.all()
        #tabla = ForumTable(foros)
    #forum_form = ForumForm()
    return render_to_response('extras/categoria.html', {'formulario': formulario,'opcion':'edit','codigo':codigo,}, context_instance=RequestContext(request),)


@login_required()
def categoria_query(request):
    col = "-name"
    query = None
    if "2-sort" in request.GET:
       col = request.GET['2-sort']
    config = RequestConfig(request)
    formulario = CategoryConsultaForm(request.GET)
    if "name" in request.GET:
        query = Category.objects.filter(name__icontains=request.GET['name']).order_by(col)
    if query is None:
        query = Category.objects.all()
    tabla = CategoryTable(query.order_by(col))
    config.configure(tabla)
    tabla.paginate(page=request.GET.get('page', 1), per_page=6)
    return render_to_response('extras/categoria_consulta.html', {'formulario':formulario,'tabla':tabla,'mensaje':(request.GET['m'] if 'm' in request.GET else '')}, context_instance=RequestContext(request),)

@login_required()
def categoria_print(request):
    if "region" in request.GET:
        qregiones = Category.objects.all().filter(name__icontains=request.GET['region']).order_by("region")
        html = render_to_string('ubigeo/reporter.html',{'data': qregiones,'pagesize':'A4','usuario':request.user.get_profile()},context_instance=RequestContext(request))
        filename= "region_%s.pdf" % datetime.today().strftime("%Y%m%d")
        return imprimirToPDF(html,filename)

@login_required()
def json_foros(request):
    if request.GET['r']:
        foros = Forum.objects.filter(category = Category.objects.get(pk = request.GET['r'])).order_by('name')
    else:
        foros = {}
    return HttpResponse(serializers.serialize("json", foros, ensure_ascii=False),mimetype='application/json')
