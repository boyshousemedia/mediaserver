from django.core.management import setup_environ
from mediaserver import settings 
setup_environ(settings)

from dashboard.models import Episode
from dashboard.utorrent_api import UTorrentConn
import sys
import subprocess

status = int(sys.argv[2])
if status == 5:
    label = sys.argv[1]

    try:
        dump,hash = label.split('-')
    except:
        dump = ''
        hash = ''

    if label == 'Colbert':
        subprocess.Popen('E:/TV/The Colbert Report/collector-p.bat', cwd='E:/TV/The Colbert Report')
    elif label == 'DailyShow':
        subprocess.Popen('E:/TV/The Daily Show/collector-p.bat', cwd='E:/TV/The Daily Show')
    elif label == 'Conan':
        subprocess.Popen('E:/TV/Conan (2010)/collector-p.bat', cwd='E:/TV/Conan (2010)')
    elif dump == "Dump":
        request = UTorrentConn("127.0.0.1:2219", "Boyshouse", "nickc")
        request.stop(hash)
        request.remove(hash)
    else:
        ep = Episode.objects.get(pk=int(label))
        ep.cleanup()
