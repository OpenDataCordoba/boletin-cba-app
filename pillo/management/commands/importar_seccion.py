import re
import shutil
import subprocess
from tempfile import NamedTemporaryFile
import urllib.request

import dateparser
from django.core.management.base import BaseCommand, CommandError
from pillo.models import SeccionBO, Publicacion


FECHA_PATTERN = re.compile('\d{1,2} de \w+ de \d{4}', flags=re.MULTILINE)
SECCION_PATTERN = re.compile('.*(\d)_Secc_\d+\.pdf$|.*\d+_seccion(\d)\.pdf$')


class Command(BaseCommand):
    help = 'Importa un pdf del boletin oficial'

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

            with urllib.request.urlopen(url) as response, NamedTemporaryFile(suffix='.pdf') as out_file:
                # Download the file from `url` and save it locally under `file_name`:
                shutil.copyfileobj(response, out_file)
                result = subprocess.run(['pdftotext', '-raw', out_file.name, '-'], stdout=subprocess.PIPE)
                texto = result.stdout.decode('utf8')
                fechas = re.findall(FECHA_PATTERN, texto)
                fecha = dateparser.parse(fechas[0], languages=['es']).date()

            obj, created = SeccionBO.objects.get_or_create(seccion=int(seccion), fecha=fecha,
                                                           defaults={'url': url, 'texto': texto})
            if created:
                print('Importado {}'.format(obj))
            else:
                print('Actualizado {}'.format(obj))
