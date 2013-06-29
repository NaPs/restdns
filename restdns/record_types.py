from django.core.exceptions import ValidationError


def validate_parameters(type, parameters):
    parameters_validators = RECORD_TYPES.get(type)
    if parameters is None:
        return parameters
    new_parameters = {}
    for name, validator in parameters_validators.iteritems():
        if name not in parameters:
            raise ValidationError({'parameters': 'Missing type parameter: %r' % name})
        else:
            try:
                new_parameters[name] = validator(parameters[name])
            except ValidationError as err:
                raise ValidationError({'parameters.%s' % name: err.message})
    return new_parameters


def check_dummy(value):
    return value


RECORD_TYPES = {'a': {'ip': check_dummy},
                'aaaa': {'ipv6': check_dummy}}