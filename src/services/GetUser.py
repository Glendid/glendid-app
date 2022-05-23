from src.commons.commons import DecimalEncoder
import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
USERS_TABLE = dynamodb.Table(os.environ['USERS_TABLE'])


def get_user_service(event, context):
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