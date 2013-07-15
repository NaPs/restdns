import sys
import json
import traceback

from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse

from .rest import RESTView
from .models import Zone, Record
from .record_types import RECORD_TYPES


class ZonesView(RESTView):

    def get(self, request, response):
        zones = [z.export() for z in Zone.objects.all()]
        return {'zones': zones}

    def post(self, request, response):
       zone = Zone(**request.body)
       zone.full_clean()
       zone.save()
       response.status = 201
       return zone.export()


class ZoneView(RESTView):

    def get(self, request, response, name):
        zone = get_object_or_404(Zone, name=name)
        return zone.export()

    def put(self, request, response, name):
        zone = get_object_or_404(Zone, name=name)
        zone.update(request.body)
        zone.full_clean()
        zone.save()
        return zone.export()

    def delete(self, request, response, name):
        zone = get_object_or_404(Zone, name=name)
        zone.delete()


class RecordsView(RESTView):

    def get(self, request, response, name):
        zone = get_object_or_404(Zone, name=name)
        records = [r.export() for r in zone.record_set.all()]
        return {'records': records}

    def post(self, request, response, name):
        zone = get_object_or_404(Zone, name=name)
        record = Record(zone=zone, **request.body)
        record.full_clean()
        record.save()
        return record.export()


class RecordView(RESTView):

    def get(self, request, response, name, record_id):
        zone = get_object_or_404(Zone, name=name)
        record = get_object_or_404(Record, id=record_id)
        if zone.id != record.zone.id:
            raise Http404()
        return record.export()

    def put(self, request, response, name, record_id):
        zone = get_object_or_404(Zone, name=name)
        record = get_object_or_404(Record, id=record_id)
        if zone.id != record.zone.id:
            raise Http404()
        record.update(request.body)
        record.full_clean()
        record.save()
        return record.export()

    def delete(self, request, response, name, record_id):
        zone = get_object_or_404(Zone, name=name)
        record = get_object_or_404(Record, id=record_id)
        if zone.id != record.zone.id:
            raise Http404()
        record.delete()


class RecordTypesView(RESTView):

    def get(self, request, response):
        return dict((k, {'parameters': v.keys()})for k, v in RECORD_TYPES.iteritems())


def error_500(request, template_name='500.html'):
    """ View defining how to report 500 errors.
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb = traceback.format_tb(exc_traceback)
    error = {'error': {'exception': str(exc_type), 'message': str(exc_value),
                       'traceback': tb}}
    return HttpResponse(json.dumps(error), statusgit=500,
                        content_type='application/json')
