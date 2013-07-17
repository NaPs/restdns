from django.conf.urls import patterns, url

from .views import ZonesView, ZoneView, RecordsView, RecordView, RecordTypesView

urlpatterns = patterns('',
    url(r'^zones/?$', ZonesView(), name='zones'),
    url(r'^zones/(?P<name>[^/]+?)/?$', ZoneView(), name='zone'),
    url(r'^zones/(?P<name>[^/]+?)/records/?$', RecordsView(), name='records'),
    url(r'^zones/(?P<name>[^/]+)/records/(?P<record_uuid>[a-f\d-]{36})/?$', RecordView(), name='record'),
    url(r'^record/types/?$', RecordTypesView(), name='record_types'),
)
