from django.conf.urls import patterns, include, url

from .views import ZonesView, ZoneView, RecordsView, RecordView

urlpatterns = patterns('',
    url(r'^zones/$', ZonesView(), name='zones'),
    url(r'^zones/(?P<name>[^/]+?)/$', ZoneView(), name='zone'),
    url(r'^zones/(?P<name>[^/]+?)/records/$', RecordsView(), name='records'),
    url(r'^zones/(?P<name>[^/]+)/records/(?P<record_id>\d+)/$', RecordView(), name='record'),
)
