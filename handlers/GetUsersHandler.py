import boto3
import json
import os

def getUsers(event, context):

    # Instanciating connection objects with DynamoDB using boto3 dependency
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')

    # Getting the table users
    USERS_TABLE = dynamodb.Table(os.environ['USERS_TABLE'])

    # Putting a try/catch to log to user when some error occurs
    try:
        response = USERS_TABLE.scan()

        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'])
        }

    except:
        print('Closing lambda function')
        return {
            'statusCode': 400,
            'body': json.dumps('Error getting users')
        }