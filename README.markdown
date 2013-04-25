Bandtastic News
===============

Este es un fork de Noticias Hacker con la intencion de tener un servicio similar para Iberoamerica y demas personas que hablen castellano y que les guste la música.

Sobre el original
-----------
Este es un clon de hacker news con la intencion de tener un servicio similar para Iberoamerica y demas personas que hablen castellano.


Instalacion
-----------

* Instalar el Google App Engine SDK
* Agregar este repositorio como un proyecto existente
* Crear un archivo llamado "keys.py". Este archivo contiene un hash para saltear los password y otros para la session. Este archivo debe de tener las siguientes dos lineas:
 



    cookie_key = 'UNASTRINGALEATORIAMUYLARGAUNASTRINGALEATORIAMUYLARGAUNASTRINGALEATORIAMUYLARGA'

    salt_key = 'UNASTRINGALEATORIAMUYLARGA'

    comment_key = 'UNASTRINGNOTANLARGAPEROSIALEATORIA'




Si quisieras usar el bot de twitter tambien necesitarias agregar las siguientes llaves de la misma manera:


    consumer_key = ""

    consumer_secret = ""

    access_token = ""

    access_token_secret = ""

    bitly_login = ''

    bitly_apikey = ''

    base_url = '' # Esto es para que solo funcione en el dominio adecuado y no en el sitio de pruebas

    base_url_custom_url = '' # Esto es si tienes un dominio diferente a appspot

    indextank_public_key = ''

    indextank_private_key = ''

    indextank_name_key = ''

    indextank_name_key_prod = ''


CSS
---

Para modificar el css requieres compilar los archivos scss con [sass](http://sass-lang.com/)

Estado actual:
--------------

El codigo esta funcionando en [Bandtastic News](http://news.bandtastic.me) 

TODO:
* Encontrar un flow de trabajo para contribuir al código de Noticias Hacker
* Agregar una manera de recuperar el password(despues de poner tu correo en el perfil)
* Agregar una manera de borrar mensajes y comentarios
* Agregar un api publico 
