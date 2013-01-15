from django.core.management import setup_environ
from mediaserver import settings

setup_environ(settings)

from dashboard.models import ServerTime, Show, Episode
from dashboard.tvdb_api import TVDBConn

serverTime = ServerTime.objects.get(pk=1)
time = serverTime.time

tvdb = TVDBConn()

print "Updating TVDB..."
print "Updating series info:"
for series in tvdb.getseriesupdates(time):
    if(Show.objects.filter(id=series).count() > 0):
        s = Show.objects.get(id=series)
        print s.name
        s.update()

print "Updating episode info:"
for episode in tvdb.getepisodeupdates(time):
    if(Episode.objects.filter(id=episode).count() > 0):
        e = Episode.objects.get(id=episode)
        print e.name
        e.update()
           
serverTime.time = tvdb.gettime()
serverTime.save() 

