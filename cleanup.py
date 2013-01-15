from django.core.management import setup_environ
from mediaserver import settings 
setup_environ(settings)

from dashboard.models import Episode
import sys
import subprocess

status = int(sys.argv[2])
if status == 5:
    label = sys.argv[1]

    if label == 'Colbert':
        subprocess.Popen('C:/TV/The Colbert Report/collector-p.bat', cwd='C:/TV/The Colbert Report')
    elif label == 'DailyShow':
        subprocess.Popen('C:/TV/The Daily Show/collector-p.bat', cwd='C:/TV/The Daily Show')
    elif label == 'Conan':
        subprocess.Popen('C:/TV/Conan (2010)/collector-p.bat]', cwd='C:/TV/Conan (2010)')
    else:
        ep = Episode.objects.get(pk=int(label))
        ep.cleanup()
