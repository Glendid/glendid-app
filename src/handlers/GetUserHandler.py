from decimal import Decimal
import boto3
import json
import os


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def get_user(event, context):
    # Instanciating connection objects with DynamoDB using boto3 dependency
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')

    # Getting the table users
    USERS_TABLE = dynamodb.Table(os.environ['USERS_TABLE'])
    print('[INPUT]:', event)

    # Putting a try/catch to log to user when some error occurs
    try:
        response = USERS_TABLE.get_item(
            Key={
                'userId': event['pathParameters']['id']
            }
        )
        print('[GET RESPONSE]:', response)
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'], cls=DecimalEncoder)
        }

    except Exception as e:
        print("Error getting user:")
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps('Error getting user')
        }