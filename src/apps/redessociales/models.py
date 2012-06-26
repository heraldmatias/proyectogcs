# -*- coding: utf-8 -*-

from django.db import models
from usuario.models import Organismo, Estado, Usuario
	
class Informacion(models.Model):
    codigo = models.AutoField(verbose_name='Codigo Autogenerado', primary_key=True)
    numinf = models.IntegerField(verbose_name='Codigo' ,unique=True)    
    organismo = models.ForeignKey(Organismo, verbose_name='Organismo')
    dependencia = models.IntegerField(verbose_name='Dependencia',)
    nombresenc = models.CharField(verbose_name='Nombres', max_length=70, )
    apellidosenc = models.CharField(verbose_name='Apellidos', max_length=70, )
    fonoenc = models.CharField(verbose_name='Teléfono', max_length=15,)
    anexoenc = models.CharField(verbose_name='Anexo', max_length=5, blank=True, null=True)
    celularenc = models.CharField(verbose_name='Celular', max_length=15)
    emailenc1 = models.EmailField(verbose_name='Email Entidad', max_length=135)
    emailenc2 = models.EmailField(verbose_name='Email Personal', max_length=135,null=True, blank=True)
    areaenc = models.CharField(verbose_name='Area', max_length=40)
    nombresjefe = models.CharField(verbose_name='Nombres', max_length=70)
    apellidosjefe = models.CharField(verbose_name='Apellidos', max_length=70)
    fonojefe = models.CharField(verbose_name='Telefono', max_length=15,)
    anexojefe = models.CharField(verbose_name='Anexo', max_length=5, blank=True, null=True)
    celularjefe = models.CharField(verbose_name='Celular', max_length=15,)
    emailjefe1 = models.EmailField(verbose_name='Email Entidad', max_length=45)
    emailjefe2 = models.EmailField(verbose_name='Email Personal', max_length=45,null=True, blank=True)
    areajefe = models.CharField(verbose_name='Area', max_length=40)
    idusuario_creac = models.ForeignKey(Usuario, verbose_name='Creador', related_name='creador')
    fec_creac = models.DateTimeField(verbose_name='Fec. Creación', auto_now_add=True)
    idusuario_mod = models.ForeignKey(Usuario,related_name='modificador',verbose_name='Modificador',null=True, blank=True)
    fec_mod = models.DateTimeField(verbose_name='Fec. Modificación',null=True, blank=True)
    class Meta:
        db_table = u'informacion'
        verbose_name = u'Informacion'
        verbose_name_plural = u'Informaciones'

    def __unicode__(self):
        return self.numinf


class Twitter(models.Model):
    codigo = models.AutoField(verbose_name='Codigo Autogenerado', primary_key=True)
    numtw = models.IntegerField(verbose_name='Codigo' ,unique=True, )
    organismo = models.ForeignKey(Organismo, verbose_name='Organismo')
    dependencia = models.IntegerField(verbose_name='Dependencia')
    fechacreac = models.DateField(verbose_name='Fecha de creación del twitter',)
    cuentatw = models.CharField(verbose_name='Cuenta oficial de Twitter', max_length=100,)
    urltw = models.URLField(verbose_name='URL cuenta Twitter(*)', max_length=150,)	
    listatw = models.IntegerField(verbose_name='Cantidad de listas del Twitter', null=True, blank=True)
    idusuario_creac = models.IntegerField(verbose_name='Numero del Usuario de creación')
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro', auto_now_add=True)
    idusuario_mod = models.IntegerField(null=True, blank=True)
    fec_mod = models.DateTimeField(null=True, blank=True,auto_now=True)
    idadministrador_mod = models.IntegerField(verbose_name='Administrador que modifico', null=True, blank=True)
    fec_modadm = models.DateTimeField(verbose_name='Fecha modificacion Administrador', auto_now=True,null=True, blank=True)
    class Meta:
        db_table = u'twitter'
        verbose_name = u'Twet'
        verbose_name_plural = u'Tweets'

    def __unicode__(self):
        return self.numtw	


class TwitterDetalle(models.Model):
    codigo = models.AutoField(verbose_name='Codigo Autogenerado', primary_key=True)
    numtw = models.ForeignKey(Twitter, verbose_name='Numero del twitter',to_field='numtw')
    item = models.IntegerField(verbose_name='Item')
    fechadettw = models.DateField(verbose_name='Fecha',)
    tweets = models.IntegerField(verbose_name='Tweets',)
    siguiendo = models.IntegerField(verbose_name='Siguiendo', blank=True, null=True)
    seguidores = models.IntegerField(verbose_name='Seguidores',)
    auditoria = models.ForeignKey(Estado, verbose_name='Estado', blank=True, null=True)
    class Meta:
        db_table = u'twitterdetalle'
        verbose_name = u'detalle del twitter'
        verbose_name_plural = u'detalles del twitter'
        unique_together = ('numtw','fechadettw',)

    def __unicode__(self):
        return self.codigo


class TwitterDiario(models.Model):
    codigo = models.AutoField(verbose_name='Codigo Autogenerado', primary_key=True)
    numtwdia = models.IntegerField(verbose_name='Codigo' ,unique=True)    
    organismo = models.ForeignKey(Organismo, verbose_name='Organismo')
    dependencia = models.IntegerField(verbose_name='Dependencia', blank=True, null=True)
    fechacreacdia = models.DateField(verbose_name='Fecha de creación',)   
    actividad = models.CharField(verbose_name='Nombre Actividad', max_length=150,)
    totaltweets = models.IntegerField(verbose_name='Tweets',)    
    totalretweets = models.IntegerField(verbose_name='Retweets',)     
    tweet1 = models.CharField(verbose_name='Nombre Tweet 1', max_length=150,)
    retweet1 = models.IntegerField(verbose_name='Retweets 1',) 
    frec1 = models.DecimalField(verbose_name='Frecuencia horas publicacion 1', max_digits=3, decimal_places=2,)
    tweet2 = models.CharField(verbose_name='Nombre Tweet 2', max_length=150,)
    retweet2 = models.IntegerField(verbose_name='Retweets 2',) 
    frec2 = models.DecimalField(verbose_name='Frecuencia horas publicacion 2', max_digits=3, decimal_places=2,)
    tweet3 = models.CharField(verbose_name='Nombre Tweet 3', max_length=150,)
    retweet3 = models.IntegerField(verbose_name='Retweets 3',) 
    frec3 = models.DecimalField(verbose_name='Frecuencia horas publicacion 3', max_digits=3, decimal_places=2,)
    tweet4 = models.CharField(verbose_name='Nombre Tweet 4', max_length=150, blank=True, null=True)
    retweet4 = models.IntegerField(verbose_name='Retweets 4', blank=True, null=True) 
    frec4 = models.DecimalField(verbose_name='Frecuencia horas publicacion 4', max_digits=3, decimal_places=2, blank=True, null=True)
    tweet5 = models.CharField(verbose_name='Nombre Tweet 5', max_length=150, blank=True, null=True)
    retweet5 = models.IntegerField(verbose_name='Retweets 5', blank=True, null=True) 
    frec5 = models.DecimalField(verbose_name='Frecuencia horas publicacion 5', max_digits=3, decimal_places=2, blank=True, null=True)
    tweet6 = models.CharField(verbose_name='Nombre Tweet 6', max_length=150, blank=True, null=True)
    retweet6 = models.IntegerField(verbose_name='Retweets 6', blank=True, null=True) 
    frec6 = models.DecimalField(verbose_name='Frecuencia horas publicacion 6', max_digits=3, decimal_places=2, blank=True, null=True)
    tweet7 = models.CharField(verbose_name='Nombre Tweet 7', max_length=150, blank=True, null=True)
    retweet7 = models.IntegerField(verbose_name='Retweets 7', blank=True, null=True) 
    frec7 = models.DecimalField(verbose_name='Frecuencia horas publicacion 7', max_digits=3, decimal_places=2, blank=True, null=True)
    tweet8 = models.CharField(verbose_name='Nombre Tweet 8', max_length=150, blank=True, null=True)
    retweet8 = models.IntegerField(verbose_name='Retweets 8', blank=True, null=True) 
    frec8 = models.DecimalField(verbose_name='Frecuencia horas publicacion 8', max_digits=3, decimal_places=2, blank=True, null=True)
    tweet9 = models.CharField(verbose_name='Nombre Tweet 9', max_length=150, blank=True, null=True)
    retweet9 = models.IntegerField(verbose_name='Retweets 9', blank=True, null=True) 
    frec9 = models.DecimalField(verbose_name='Frecuencia horas publicacion 9', max_digits=3, decimal_places=2, blank=True, null=True)
    tweet10 = models.CharField(verbose_name='Nombre Tweet 10', max_length=150, blank=True, null=True)
    retweet10 = models.IntegerField(verbose_name='Retweets 10', blank=True, null=True) 
    frec10 = models.DecimalField(verbose_name='Frecuencia horas publicacion 10', max_digits=3, decimal_places=2, blank=True, null=True)
    tweetvarios = models.IntegerField(verbose_name='Tweets varios', blank=True, null=True)    
    retweetvarios = models.IntegerField(verbose_name='Retweets varios', blank=True, null=True)  
    idusuario_creac = models.IntegerField(verbose_name='Usuario',)
    class Meta:
        db_table = u'twitterdiario'
        verbose_name = u'Twitter Diario'
        verbose_name_plural = u'Twitter Diarios'

    def __unicode__(self):
        return self.actividad

class Facebook(models.Model):
    codigo = models.AutoField(verbose_name='Codigo Autogenerado', primary_key=True)
    numfb = models.IntegerField(verbose_name='Codigo' ,unique=True)    
    organismo = models.ForeignKey(Organismo, verbose_name='Organismo')
    dependencia = models.IntegerField(verbose_name='Dependencia', blank=True, null=True)
    fechacreac = models.DateField(verbose_name='Fecha de creación del Facebook',)
    cuentafb = models.CharField(verbose_name='Cuenta Oficial', max_length=100,)
    urlfb = models.CharField(verbose_name='URL Oficial', max_length=150,)
    idusuario_creac = models.IntegerField(verbose_name='Numero del Usuario de creación')
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro', auto_now_add=True)
    idusuario_mod = models.IntegerField(null=True, blank=True)
    fec_mod = models.DateTimeField(null=True, blank=True,auto_now=True)
    idadministrador_mod = models.IntegerField(verbose_name='Administrador que modifico', blank=True, null=True)
    fec_modadm = models.DateTimeField(verbose_name='Fecha modificacion Administrador', auto_now=True,)	
    class Meta:
        db_table = u'facebook'
        verbose_name = u'cuenta de facebook'
        verbose_name_plural = u'cuentas de facebook'

    def __unicode__(self):
        return self.codigo
	
class FacebookDetalle(models.Model):
    codigo = models.AutoField(verbose_name='Codigo Autogenerado', primary_key=True)
    numfb = models.ForeignKey(Facebook, verbose_name='Numero del Facebook',to_field='numfb')
    item = models.IntegerField(verbose_name='Numero de items')
    fechadetfb = models.DateField(verbose_name='Fecha de los Likes',)
    cantidad = models.IntegerField(verbose_name='Numero de Likes',)
    auditoria = models.ForeignKey(Estado, verbose_name='Estado', blank=True, null=True)
    class Meta:
        db_table = u'facebookdetalle'
        verbose_name = u'detalle del post'
        verbose_name_plural = u'detalles de los post'
        unique_together = ('numfb','fechadetfb',)

    def __unicode__(self):
        return self.codigo


class FacebookDiario(models.Model):
    codigo = models.AutoField(verbose_name='Codigo Autogenerado', primary_key=True)
    numfbdia = models.IntegerField(verbose_name='Codigo', unique=True)    
    organismo = models.ForeignKey(Organismo, verbose_name='Organismo')
    dependencia = models.IntegerField(verbose_name='Dependencia', blank=True, null=True)
    fechacreacdia = models.DateField(verbose_name='Fecha de creación',)   
    actividad = models.CharField(verbose_name='Nombre Actividad', max_length=150,)
    totalpost = models.IntegerField(verbose_name='Posts',)    
    totallikes = models.IntegerField(verbose_name='Likes',)
    totalcompartido = models.IntegerField(verbose_name='Total Compartidos',)
    totalcomentario = models.IntegerField(verbose_name='Total Comentarios',)
    totalfotogaleria = models.IntegerField(verbose_name='Total de fotografías',)
    totallikegaleria = models.IntegerField(verbose_name='Total Likes Galeria',)
    totalcomentariogaleria = models.IntegerField(verbose_name='Total Comentarios Galeria',)
    totalcompartidogaleria = models.IntegerField(verbose_name='Total compartido galeria',)
    post1 = models.CharField(verbose_name='Nombre Post 1', max_length=150, )
    like1 = models.IntegerField(verbose_name='Numero Likes 1',  ) 
    compartido1 = models.IntegerField(verbose_name='Numero Compartidas 1',  ) 
    comentario1 = models.IntegerField(verbose_name='Numero comentarios 1',  ) 
    post2 = models.CharField(verbose_name='Nombre Post 2', max_length=150,  )
    like2 = models.IntegerField(verbose_name='Numero Likes 2',  ) 
    compartido2 = models.IntegerField(verbose_name='Numero Compartidas 2',  ) 
    comentario2 = models.IntegerField(verbose_name='Numero comentarios 2',  ) 
    post3 = models.CharField(verbose_name='Nombre Post 3', max_length=150,  )
    like3 = models.IntegerField(verbose_name='Numero Likes 3',  ) 
    compartido3 = models.IntegerField(verbose_name='Numero Compartidas 3',  ) 
    comentario3 = models.IntegerField(verbose_name='Numero comentarios 3',  ) 
    post4 = models.CharField(verbose_name='Nombre Post 4', max_length=150, blank=True, null=True,)
    like4 = models.IntegerField(verbose_name='Numero Likes 4', blank=True, null=True,) 
    compartido4 = models.IntegerField(verbose_name='Numero Compartidas 4', blank=True, null=True,) 
    comentario4 = models.IntegerField(verbose_name='Numero comentarios 4', blank=True, null=True,) 
    post5 = models.CharField(verbose_name='Nombre Post 5', max_length=150, blank=True, null=True,)
    like5 = models.IntegerField(verbose_name='Numero Likes 5', blank=True, null=True,) 
    compartido5 = models.IntegerField(verbose_name='Numero Compartidas 5', blank=True, null=True,) 
    comentario5 = models.IntegerField(verbose_name='Numero comentarios 5', blank=True, null=True,) 
    post6 = models.CharField(verbose_name='Nombre Post 6', max_length=150, blank=True, null=True,)
    like6 = models.IntegerField(verbose_name='Numero Likes 6', blank=True, null=True,) 
    compartido6 = models.IntegerField(verbose_name='Numero Compartidas 6', blank=True, null=True,) 
    comentario6 = models.IntegerField(verbose_name='Numero comentarios 6', blank=True, null=True,) 
    post7 = models.CharField(verbose_name='Nombre Post 7', max_length=150, blank=True, null=True,)
    like7 = models.IntegerField(verbose_name='Numero Likes 7', blank=True, null=True,) 
    compartido7 = models.IntegerField(verbose_name='Numero Compartidas 7', blank=True, null=True,) 
    comentario7 = models.IntegerField(verbose_name='Numero comentarios 7', blank=True, null=True,) 
    post8 = models.CharField(verbose_name='Nombre Post 8', max_length=150, blank=True, null=True,)
    like8 = models.IntegerField(verbose_name='Numero Likes 8', blank=True, null=True,) 
    compartido8 = models.IntegerField(verbose_name='Numero Compartidas 8', blank=True, null=True,) 
    comentario8 = models.IntegerField(verbose_name='Numero comentarios 8', blank=True, null=True,) 
    post9 = models.CharField(verbose_name='Nombre Post 9 ', max_length=150, blank=True, null=True,)
    like9 = models.IntegerField(verbose_name='Numero Likes 9', blank=True, null=True,) 
    compartido9 = models.IntegerField(verbose_name='Numero Compartidas 9', blank=True, null=True,) 
    comentario9 = models.IntegerField(verbose_name='Numero comentarios 9', blank=True, null=True,) 
    post10 = models.CharField(verbose_name='Nombre Post 10', max_length=150, blank=True, null=True,)
    like10 = models.IntegerField(verbose_name='Numero Likes 10', blank=True, null=True,) 
    compartido10 = models.IntegerField(verbose_name='Numero Compartidas 10', blank=True, null=True,) 
    comentario10 = models.IntegerField(verbose_name='Numero comentarios 10', blank=True, null=True,) 
    postvarios = models.IntegerField(verbose_name='Post varios',null=True, blank=True)    
    likevarios = models.IntegerField(verbose_name='Les gusta varios',null=True, blank=True)
    compartidovarios = models.IntegerField(verbose_name='Compartido varios',null=True, blank=True)    
    comentariovarios = models.IntegerField(verbose_name='Comentarios varios',null=True, blank=True)  
    idusuario_creac = models.IntegerField(verbose_name='Usuario')
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro', auto_now_add=True)
    idusuario_mod = models.IntegerField(null=True, blank=True)
    fec_mod = models.DateTimeField(null=True, blank=True)
    idadministrador_mod = models.IntegerField(verbose_name='Administrador que modifico',null=True, blank=True)
    fec_modadm = models.DateTimeField(verbose_name='Fecha modificacion Administrador', auto_now_add=True)
    class Meta:
        db_table = u'facebookdiario'
        verbose_name = u'Facebook Diario'
        verbose_name_plural = u'Facebook Diarios'

    def __unicode__(self):
        return self.actividad
