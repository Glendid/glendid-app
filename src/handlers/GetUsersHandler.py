from src.services.GetUsers import get_users_service
from src.commons.commons import get_request


def get_users(event, context):
    print('[INPUT]:', event)
    request = get_request(event)
    return get_users_service(request)

