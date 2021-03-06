
import json

from django.db import models

from south.modelsinspector import add_introspection_rules


class JSONField(models.TextField):

    """ Custom field used to store JSON data.
    """

    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if isinstance(value, basestring):
            value = json.loads(value)
        return value

    def get_prep_value(self, value):
        return json.dumps(value)


add_introspection_rules([], ["^restdns\.fields\.JSONField"])