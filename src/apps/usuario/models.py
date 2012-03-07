# -*- coding: utf-8 -*-

from django.db import models

SEXO = (
        ('FE','Femenino'),
        ('MA','Masculino'),
        )

class Estado(models.Model):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=45)
    class Meta:
        db_table = u'estado'
        verbose_name = u'Estado'
        verbose_name_plural = u'Estados'

class Nivel(models.Model):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=45)
    class Meta:
        db_table = u'nivel'
        verbose_name = u'Nivel'
        verbose_name_plural = u'Niveles'

class Organismo(models.Model):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=105)
    class Meta:
        db_table = u'organismo'
        verbose_name = u'Organismo'
        verbose_name_plural = u'Organismos'

class Usuario(models.Model):
    codigo = models.AutoField(primary_key=True)
    numero = models.IntegerField(unique=True)
    nivel = models.ForeignKey(Nivel, verbose_name='Nivel')
    organismo = models.IntegerField(verbose_name='Organismo', blank=True, null=True)
    dependencia = models.ForeignKey(Organismo, verbose_name='Dependencia')
    nombre = models.CharField(max_length=75, blank=True, null=True)
    apellido = models.CharField(max_length=150,  blank=True, null=True)
    sexo = models.CharField(max_length=2,choices = SEXO, blank=True, null=True)
    usuario = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=135)
    contrasena = models.CharField(max_length=96)
    emailalt = models.CharField(max_length=135)
    fono = models.CharField(max_length=75, blank=True)
    anexo = models.CharField(max_length=30, blank=True)
    rpm = models.CharField(max_length=75, blank=True)
    rpc = models.CharField(max_length=75, blank=True)
    nextel = models.CharField(max_length=75, blank=True)
    twitter = models.CharField(max_length=120, blank=True)
    facebook = models.CharField(max_length=75, blank=True)
    estado = models.ForeignKey(Estado, verbose_name='Organismo')
    politica = models.IntegerField(null=True, blank=True)
    idusuario_mod = models.IntegerField(null=True, blank=True)
    fec_mod = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'usuario'
        verbose_name = u'Usuario'
        verbose_name_plural = u'Usuarios'

