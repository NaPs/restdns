import re

from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv4_address, validate_ipv6_address


RE_NAME = re.compile(r'^([\w]{1,2}|[\w][\w-]{0,61}[\w])'
                     r'([.]([\w]{1,2}|[\w][\w-]{0,61}[\w]))*[.]?$')


def validate_parameters(type, parameters):
    parameters_validators = RECORD_TYPES.get(type)
    if parameters is None:
        return parameters
    new_parameters = {}
    for name, validator in parameters_validators.iteritems():
        if name not in parameters:
            raise ValidationError({'parameters': ['Missing type parameter: %r' % name]})
        else:
            try:
                validated = validator(parameters[name])
                if validated is not None:
                    new_parameters[name] = validated
                else:
                    new_parameters[name] = parameters[name]
            except ValidationError as err:
                raise ValidationError({'parameters.%s' % name: err.messages})
    return new_parameters


def validate_name(value):
    value = str(value)
    if len(value) > 255:
        raise ValidationError('Name is too long')
    elif not RE_NAME.match(value):
        raise ValidationError('Bad name')


def validate_int(value):
    value = int(value)
    if not 0 <= value <= 65535:
        raise ValidationError('Bad value, must be between the range 0-65535')


RECORD_TYPES = {'a': {'ip': validate_ipv4_address},
                'aaaa': {'ipv6': validate_ipv6_address},
                'cname': {'name': validate_name},
                'mx': {'pref': validate_int, 'name': validate_name},
                'ns': {'name': validate_name},
                'srv': {'priority': validate_int, 'weight': validate_int,
                        'port': validate_int, 'target': validate_name},
                'txt': {'text': lambda x:x},
                'hinfo': {'hardware': lambda x:x, 'os': lambda x:x},
                'ptr': {'name': validate_name},
                'spf': {'text': lambda x:x}}
