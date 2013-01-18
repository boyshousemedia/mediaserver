from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mediaserver.views.home', name='home'),
    # url(r'^mediaserver/', include('mediaserver.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     url(r'^dashboard/$', 'dashboard.views.index'),
     url(r'^dashboard/shows/$', 'dashboard.views.shows'),
     url(r'^dashboard/shows/search/$', 'dashboard.views.search'),
     url(r'^dashboard/shows/add/$', 'dashboard.views.add'),
     url(r'^dashboard/shows/seasons/$', 'dashboard.views.seasons'),
     url(r'^dashboard/shows/downloadtoggle/$', 'dashboard.views.downloadtoggle'),
     url(r'^dashboard/shows/remove/$', 'dashboard.views.downloadtoggle'),
     url(r'^dashboard/shows/gettorrents/$', 'dashboard.views.gettorrents'),
     url(r'^dashboard/shows/setsearch/$', 'dashboard.views.setsearch'),
     url(r'^dashboard/shows/recent/$', 'dashboard.views.recent'),
     url(r'^dashboard/shows/download/$', 'dashboard.views.download'),
     url(r'^dashboard/utorrent/$', 'dashboard.views.utorrent'),
     url(r'^dashboard/utorrent/update$', 'dashboard.views.update'),
)
