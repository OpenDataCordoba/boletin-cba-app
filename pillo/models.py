from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

class SeccionBO(models.Model):
    SECCIONES = (
        (1, "1º Sección: Legislación – Normativas"),
        (2, "2º Sección: Judiciales"),
        (3, "3º Sección: Sociedades – Personas Jurídicas – Asambleas y Otras"),
        (4, "4º Sección: Concesiones, Licitaciones, Servicios Publ. y Contrataciones"),
        (5, "5º Sección: Municipalidades y Comunas: Legislación – Normativas"),
    )
    seccion = models.CharField(max_length=20, choices=SECCIONES)
    fecha = models.DateField()
    texto = models.TextField(help_text='texto crudo, conversion del pdf')
    url = models.URLField(help_text='url original del pdf')

    def __str__(self):
        return '{}º seccion del {}'.format(self.seccion, self.fecha)

    class Meta:
        unique_together = (("seccion", "fecha"),)


class Publicacion(models.Model):
    bo = models.ForeignKey('SeccionBO')
    texto = models.TextField(help_text='Fragmento de texto extraido del texto de la seccion')
    pagina = models.PositiveIntegerField(null=True, blank=True,
        help_text='Nº pagina donde comienza esta publicacion en la seccion')
    metadatos = JSONField(help_text="contiene informacion estructurada", null=True, blank=True)
