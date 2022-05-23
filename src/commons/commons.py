def validate_fields(request, required_fields):
    for key in request:
        if required_fields.count(key):
            return request
        raise Exception(key, ' is required')
