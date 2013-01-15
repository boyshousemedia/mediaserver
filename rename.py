from django.core.management import setup_environ
from mediaserver import settings 
setup_environ(settings)

from dashboard.models import Episode
eps = Episode.objects.filter(path='pending')
for ep in eps:
    ep.rename()

