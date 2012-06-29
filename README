------------------------
Instalación
------------------------
1.- sudo apt-get install python-dev
2.- python bootstrap.py -d
3.- bin/buildout -vvv
4.- rm -fr eggs/pybbm-0.8.2-py2.6.egg/pybb/
5.- cp -R src/apps/pybb/ eggs/pybbm-0.8.2-py2.6.egg/
6.- mkdir media
7.- Dar permisos de lectura y escritura en la carpeta media al usuario del sistema dueño de la aplicacion.
8.- configurar la base de datos project/settings.py
9.- bin/ogcs syncdb
10.- bin/ogcs migrate pybb
11.- bin/ogcs collectstatic
12.- Modificar el nombre del sitio con el nombre del DOMINIO donde se aloja la web desde el admin.


------------------------



