from src.services.DeleteUser import delete_user_service


def delete_user(event, context):
    print('[DELETE INPUT]:', event)
    return delete_user_service(event, context)
