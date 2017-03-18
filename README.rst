Aplicacion web para navegar el boletin oficial cordoba
------------------------------------------------------

Usa python 3.5+


- Configurar base de datos postgresql  (basado en local_settings.py.template) en boc/local_settings.py

- instalar requirements  (pip install -r requirements)
- python manage.py migrate


Para importar una seccion del boletin ::


python manage.py importar_seccion <url_al_pdf>


