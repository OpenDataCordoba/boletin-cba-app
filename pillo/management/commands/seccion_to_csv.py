import re
import csv

from django.core.management.base import BaseCommand, CommandError
from pillo.models import SeccionBO, Publicacion


FECHA_PATTERN = re.compile('\d{1,2} de \w+ de \d{4}', flags=re.MULTILINE)
SECCION_PATTERN = re.compile('.*(\d)_Secc_\d+\.pdf$|.*\d+_seccion(\d)\.pdf$')


class Command(BaseCommand):
    help = 'Importa un documento del boletin oficial en la DB a CSV'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='+', type=str)

    def handle(self, *args, **options):
        for url in options['url']:
            # encuentra el tipo de seccion del BO a partir de la url
            for seccion in re.match(SECCION_PATTERN, url).groups():
                if seccion:
                    break
            if not seccion:
                raise CommandError('Url incorrecta, no se reconoce seccion')

            # TODO: Revisar identificador unico de boletin.
            # Hay casos de urls duplicados guardados con distinta fecha
            obj = SeccionBO.objects.filter(url=url)[0]
            fecha = obj.fecha.strftime('%Y-%b-%d')

            with open(''.join([fecha + '_' + obj.seccion, '.csv']), 'w+') as csvfile:
                seccion_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
                seccion_writer.writerow([obj.id, obj.seccion, obj.fecha, obj.texto, obj.url])
