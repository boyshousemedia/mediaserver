from django.core.management import setup_environ
from mediaserver import settings

setup_environ(settings)

from dashboard.models import ServerTime, Show, Episode
from dashboard.tvdb_api import TVDBConn

serverTime = ServerTime.objects.get(pk=1)
time = serverTime.time

tvdb = TVDBConn()
updates_day = tvdb.getupdates_day()
newTime = updates_day['@time']

print "Updating TVDB..."
print "Updating series info:"
for series in updates_day['Series']:
    if(int(series['time']) > time):
        if(Show.objects.filter(id=series['id']).count() > 0):
            s = Show.objects.get(id=series['id'])
            print s.name
            s.update()

print "Updating episode info:"
for episode in updates_day['Episode']:
    if(int(episode['time']) > time):
        if(Episode.objects.filter(id=episode['id']).count() > 0):
            e = Episode.objects.get(id=episode['id'])
            print e.show_name + ": " + e.name
            e.update()
        elif(Show.objects.filter(id=episode['Series']).count() > 0):
            s = Show.objects.get(id=episode['Series'])
            ep = tvdb.getepisodebyid(episode['id'])
            print "Creating " + s.name + ": " + Episode.getField(ep, 'EpisodeName', '(No name)')
            Episode.create(ep, episode['Series'], s.name)
           
serverTime.time = newTime
serverTime.save()
print "time saved"

