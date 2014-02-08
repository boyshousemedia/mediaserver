from django.core.management import setup_environ
from mediaserver import settings
setup_environ(settings)

from dashboard.models import Episode, Show
from dashboard.tvdb_api import TVDBConn

def update_show(name):
    print '\n' + name
    try:
        show = Show.objects.get(name=name)
        show_id = show.id
    except:
        print name + " could not be found"
        return

    cur_eps_full = Episode.objects.filter(show_name=name)
    cur_eps = []
    for ep in cur_eps_full:
        cur_eps.append(int(ep.id))

    tvdb = TVDBConn()
    series = tvdb.initseriesbyid(str(show.id))
    new_eps = series['Episode']
    new_eps_ids = []
    for ep in new_eps:
        new_eps_ids.append(int(ep['id']))

    # identify removed eps
    for ep in cur_eps:
        if ep not in new_eps_ids:
            ep_full = Episode.objects.get(id=ep)
            print ep_full.name + ' removed'
            if not ep_full.path:
                ep_full.delete()
            else:
                print 'has file'

    for ep in new_eps:
        # identify new eps
        if int(ep['id']) not in cur_eps:
            print repr(ep['EpisodeName']) + ' new'
            Episode.create(ep, show_id, name)

        # update existing eps
        else:
            existing = Episode.objects.get(id=int(ep['id']))
            existing.update(ep)

shows = Show.objects.all()
for i, show in enumerate(shows):
    name = show.name
    update_show(name)

    print '%s of %s complete.' % (i+1, len(shows))
