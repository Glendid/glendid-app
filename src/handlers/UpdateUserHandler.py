from boto3.dynamodb.conditions import Key
import datetime
import boto3
import json
import os
import time

dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
USERS_TABLE = dynamodb.Table(os.environ['USERS_TABLE'])


def update_user(event, context):
    print('[INPUT]:', event)
    body = event['body']
    request = json.loads(body)
    required_fields = ['address', 'admissionDate', 'documentNumber', 'documentType', 'email', 'role',
                       'telephoneNumber']
    validate_fields(request, required_fields)

    response = USERS_TABLE.get_item(
        Key={
            'userId': event['pathParameters']['id']
        }
    )

    print("[GET RESPONSE]", response)

    user_data: object = {
        'active': True,
        'address': request['address'],
        'admissionDate': convert_to_unix(request['admissionDate']),
        'assigned': request.get('assigned', []),
        'birthDate': convert_to_unix(request.get('birthDate', '')),
        'clientName': request.get('clientName', ''),
        'created': response['Item']['created'],
        'description': request.get('description', ''),
        'documentNumber': response['Item']['documentNumber'],
        'documentType': response['Item']['documentType'],
        'email': request['email'],
        'firstName': request.get('firstName', ''),
        'lastName': request.get('lastName', ''),
        'occupation': request.get('occupation', ''),
        'role': request['role'],
        'size': request.get('size', ''),
        'telephoneNumber': request['telephoneNumber'],
        'updated': int(time.time()),
        'userId': event['pathParameters'].get('id')
    }

    try:
        USERS_TABLE.put_item(
            Item=user_data
        )

        return {
            'statusCode': 200,
            'body': json.dumps('User updated.')
        }
    except Exception as e:
        print("Error creating user")
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps('Error updating the user')
        }


def getuser(document_number):
    response = USERS_TABLE.query(
        IndexName='documentNumberIndex',
        KeyConditionExpression=Key('documentNumber').eq(document_number)
    )
    print('[QUERY RESPONSE]:', response)
    for item in response['Items']:
        if document_number in item:
            raise Exception('User already exist.')
        return True


def convert_to_unix(date):
    if date != '':
        return int(datetime.datetime.strptime(date, "%d/%m/%Y").timestamp())
    return ''


def validate_fields(request, required_fields):
    for key in request:
        if required_fields.count(key):
            return request
        raise Exception(key, ' is required')
