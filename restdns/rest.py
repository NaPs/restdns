import json

from django.http import HttpResponse, Http404
from django.core.exceptions import ValidationError


class JsonHttpRequestWrapper(object):

    def __init__(self, request):
        self._request = request

    @property
    def body(self):
        if 'application/json' in self._request.META['CONTENT_TYPE']:  #QUIRK: proper way to parse content type
            return json.loads(self._request.body)
        else:
            return self._request.body

    def __getattr__(self, attr):
        return self._request.__getattribute__(attr)


class RESTView(object):

    """ Base class for class-based REST views.
    """

    def __call__(self, request, *args, **kwargs):
        view = getattr(self, request.method.lower(), None)
        if view is None:
            return HttpResponse(status=400)
        else:
            response = HttpResponse(status=200)
            try:
                output = view(JsonHttpRequestWrapper(request), response, *args, **kwargs)
            except ValidationError as err:
                output = {'error': err.message_dict}
                response.status_code = 400
            except Http404:
                output = {'error': 'Not found'}
                response.status_code = 404
            if output is None:
                response.status_code = 204
            else:
                indent = 4 if 'pretty' in request.GET else None
                response.write(json.dumps(output, indent=indent))
                response['Content-Type'] = 'application/json'
        return response