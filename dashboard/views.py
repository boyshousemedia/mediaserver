from django.shortcuts import render_to_response
from dashboard.models import Episode, Show, ServerTime
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.db.models import Q
from django.db.models import Max

from tvdb_api import TVDBConn

def index(request):
    return render_to_response('dashboard/index.html')

def shows(request):
    shows = Show.objects.all().order_by('name')
    return render_to_response('dashboard/shows.html', {'shows' : shows})

def downloadtoggle(request):
    show_id = request.GET.get('id')
    show = Show.objects.get(id=show_id)
    show.toggleDownload()
    show.save()
    return HttpResponse()

def search(request):

    class SearchResult:
        def __init__(self, seriesid, seriesname, overview):
            self.seriesid = seriesid
            self.seriesname = seriesname
            self.overview = overview

    tvdb = TVDBConn()
    searchtext = request.GET.get('searchtext')
    shows = []
    for result in tvdb.lookup(searchtext.replace("+"," ")):
        shows.append( SearchResult(result['seriesid'], result['SeriesName'], result.get('Overview', 'No overview available.')) )
    return render_to_response('dashboard/search.html', {'shows' : shows})

def gettorrents(request):
    ep_id = request.GET.get('id')
    ep = Episode.objects.get(id=ep_id)
    url = ep.getSearchUrl()
    torrents = ep.gettorrents()[:5]
    return render_to_response('dashboard/torrents.html', {'torrents' : torrents, 'url' : url})

def download(request):
    ep_id = request.GET.get('id')
    link = request.GET.get('link')
    ep = Episode.objects.get(id=ep_id)
    ep.download(link)
    return HttpResponse()

def add(request):
    show_id = request.GET.get('id')
    Show.create(show_id)
    return HttpResponse()

def update():
    serverTime = ServerTime.objects.get(pk=1)
    time = serverTime.time

    tvdb = TVDBConn()
    for series in tvdb.getseriesupdates(time):
        if(Show.objects.filter(id=series).count() > 0):
            s = Show.objects.get(id=series)
            s.update()
    for episode in tvdb.getepisodeupdates(time):
        if(Episode.objects.filter(id=episode).count() > 0):
            e = Episode.objects.get(id=episode)
            e.update()

    serverTime.time = tvdb.gettime()
    serverTime.save()

def setsearch(request):
    show_id = request.GET.get('id')
    search = request.GET.get('search')
    show = Show.objects.get(id=show_id)
    show.search = search
    show.save()
    return HttpResponse()
    
def seasons(request):
    show_id = request.GET.get('id')
    season = request.GET.get('season')

    # 0 means choose most recent season
    if (season == '0'):
        recent = Episode.objects.filter(show_id=show_id).filter(air_date__gte=datetime.now()).order_by('air_date')
        if (len(recent) > 0):
            season = recent[0].season
        else:
            season =  Episode.objects.filter(show_id=show_id).aggregate(Max('season')).get('season__max')

    episodes = Episode.objects.filter(show_id=show_id).filter(~Q(season = 0)).order_by('season', 'number')
    num_seasons = Episode.objects.filter(show_id=show_id).aggregate(Max('season')).get('season__max')
    show = Show.objects.get(id=show_id)
    return render_to_response('dashboard/seasons.html', {'episodes' : episodes, 
                                                        'season' : season,
                                                        'show' : show,
                                                        'num_seasons' : map(lambda x:x+1, range(num_seasons))})

def recent(request):
    class DayShows:
        def __init__(self):
            self.eps = []

        def add(self, ep):
            self.day = ep.air_date
            self.eps.append(ep)
    
    week_ago = datetime.now() - timedelta(weeks=1)
    eps = Episode.objects.filter(air_date__gt=week_ago).filter(air_date__lt=datetime.now()).order_by('-air_date')
    
    days = []
    dayShows = None
    day = -1
    for ep in eps:
        if ep.air_date.weekday() != day:
            if dayShows != None:
                days.append(dayShows)
            dayShows = DayShows()
        dayShows.add(ep)

    # Grab last dayshow
    if (not dayShows == None):
        days.append(dayShows)

    return render_to_response('dashboard/recent.html', {'days' : days }) 

