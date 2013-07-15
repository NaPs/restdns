from django.conf.urls import patterns, include, url

from .views import (ZonesView, ZoneView, RecordsView, RecordView,
                    RecordTypesView, error_500)


urlpatterns = patterns('',
    url(r'^zones/$', ZonesView(), name='zones'),
    url(r'^zones/(?P<name>[^/]+?)/$', ZoneView(), name='zone'),
    url(r'^zones/(?P<name>[^/]+?)/records/$', RecordsView(), name='records'),
    url(r'^zones/(?P<name>[^/]+)/records/(?P<record_id>\d+)/$', RecordView(), name='record'),
    url(r'^record/types/$', RecordTypesView(), name='record_types'),
)

handler500 = error_500
