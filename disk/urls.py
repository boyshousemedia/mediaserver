from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', 'disk.views.disk', name='disk'),
                       url(r'^update/$', 'disk.views.update_disks', name='update_disks'),
                       )