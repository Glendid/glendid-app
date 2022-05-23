from src.services.GetUser import get_user_service


def get_user(event, context):
    print('[INPUT GET USER]:', event)
    return get_user_service(event, context)
