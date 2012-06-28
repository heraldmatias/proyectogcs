# -*- coding: utf-8 -*-
from django.db import models
from usuario.models import Organismo, Usuario

CATEGORIAS = (
    ('OTROS','OTROS'),
    ('IMAGENES','IMAGENES'),
    ('VIDEOS','VIDEOS'),
    ('AUDIOS','AUDIOS'),
    ('DOCUMENTOS','DOCUMENTOS'),
    ('COMPRIMIDOS','COMPRIMIDOS'),
)

EXTENSIONES = (
    ('OTROS',(
        ('OTRO','OTRO'),
        )
    ),
    ('IMAGENES',(
        ('JPG','JPG'),('GIF','GIF'),('ICO','ICO'),('PNG','PNG'),('TIF','TIF')
        )
    ),  
    ('VIDEOS',(
        ('AVI','AVI'),('MOV','MOV'),('MP4','MP4'),('WMV','WMV'),('FLV','FLV'),('F4V','F4V'),('3GP','3GP'),
        )
    ),
    ('AUDIOS',(
        ('MP3','MP3'),('WAV','WAV'),('AMF','AMF'),('AMV','AMV'),('OGG','OGG'),
        )
    ),
    ('DOCUMENTOS',(
        ('DOC','DOC'),('DOCX','DOCX'),('PDF','PDF'),('PPT','PPT'),('PPTX','PPTX'),('XLS','XLS'),('XLSX','XLSX'),('TXT','TXT'),('ODT','ODT'),
        )
    ),
    ('COMPRIMIDOS',(
        ('ZIP','ZIP'),('TAR','TAR'),('GZ','GZ'),('ZIP','ZIP'),('RAR','RAR'),('7Z','7Z'),
        )
    ),
)

class Documento(models.Model):
    codigo = models.AutoField(verbose_name='Codigo', primary_key=True)
    organismo = models.ForeignKey(Organismo, verbose_name='Organismo')
    dependencia = models.IntegerField(verbose_name='Dependencia',)
    archivo = models.FileField(verbose_name ='Adjuntar Archivo', upload_to='documentos')
    url_archivo = models.URLField(verbose_name='URL del Archivo',null=True, blank=True)
    tipo = models.CharField(verbose_name = 'Tipo',max_length=5,choices=EXTENSIONES)
    categoria = models.CharField(verbose_name = 'Categoria',choices=CATEGORIAS,max_length=50)
    idusuario_creac = models.ForeignKey(Usuario, verbose_name='Usuario',)
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro',auto_now_add=True)

    class Meta:
        db_table = u'documentos'
        verbose_name = u'Documento'
        verbose_name_plural = u'Documentos'
        permissions = (
            ('query_documento','Puede Consultar Documento'),
        )

    def __unicode__(self):
        return self.archivo
