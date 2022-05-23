from src.commons.commons import validate_fields, get_request
from src.services.CreateUser import create_user_service


def create_user(event, context):
    print('[CREATE INPUT]:', event)
    request = get_request(event)
    required_fields = ['address', 'admissionDate', 'documentNumber', 'documentType', 'email', 'role',
                       'telephoneNumber']
    validate_fields(request, required_fields)
    return create_user_service(request)

