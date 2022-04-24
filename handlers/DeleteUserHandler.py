import boto3
import json
import os

def deleteUser(event, context):

    data = json.loads(event['body'])
    if 'userId' not in data or 'active' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't delete the user item please specify the user id.")
        return

    #Instanciating connection objects with DynamoDB using boto3 dependency
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')

    # Getting the table users
    USERS_TABLE = dynamodb.Table(os.environ['USERS_TABLE'])

    # Putting a try/catch to log to user when some error occurs
    try:

        response = USERS_TABLE.update_item(
            Key={
                "userId": data['userId'],
            },
            ExpressionAttributeValues= {
                ":a": data['active'],
            },
            UpdateExpression= "set active = :a ",
            ReturnValues="UPDATED_NEW",
        )
        # create a response
        return {
            'statusCode': 200,
            'body': json.dumps('ok deleted')
        }

    except:
        print('Closing lambda function')
        return {
            'statusCode': 400,
            'body': json.dumps("Error deleting users")
        }