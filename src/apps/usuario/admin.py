from django.contrib import admin
from models import Estado, Nivel, Organismo, Usuario

class ModelUsuario(admin.ModelAdmin):    
    list_display = ('codigo','numero','apellido','nombre','fono',)
    list_display_links = ('codigo','apellido','nombre',)
    list_filter = ('nombre','apellido',)
    search_fields = ['^nombre','^apellido']
    list_per_page= 25
    list_max_show_all=50
    fieldsets = (
        ('Datos Personales', {
            'classes': ('collapse',),
            'description':'Rellene los campos con la informacion personal del Alumno',
            'fields': ('numero',('nombre', 'apellido',), ('sexo',),)
        }),
        ('Datos Adicionales', {
            'classes': ('collapse',),
	    'description':'Rellene la informacion adicional del alumno, algunos campos son opcionales', 	
            'fields': (('fono','rpm',),('rpc','nextel'), ('facebook','twitter',),)
        }),        
    )

admin.site.register(Usuario,ModelUsuario)
