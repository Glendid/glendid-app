from boto3.dynamodb.conditions import Key
import datetime
import boto3
import json
import os
import time
import uuid
import logging

# Instanciating connection objects with DynamoDB using boto3 dependency
dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
# Getting the table users
USERS_TABLE = dynamodb.Table(os.environ['USERS_TABLE'])


def create_user(event, context):
    print('[INPUT]:', event)
    body = event['body']
    request = json.loads(body)
    required_fields = ['address', 'admissionDate', 'documentNumber', 'documentType', 'email', 'role',
                       'telephoneNumber']
    validate_fields(request, required_fields)
    getuser(request['documentNumber'])

    user_data: object = {
        'active': True,
        'address': request['address'],
        'admissionDate': convert_to_unix(request['admissionDate']),
        'assigned': request.get('assigned', []),
        'birthDate': convert_to_unix(request.get('birthDate', '')),
        'clientName': request.get('clientName', ''),
        'created': int(time.time()),
        'description': request.get('description', ''),
        'documentNumber': request['documentNumber'],
        'documentType': request['documentType'],
        'email': request['email'],
        'firstName': request.get('firstName', ''),
        'lastName': request.get('lastName', ''),
        'occupation': request.get('occupation', ''),
        'role': request['role'],
        'size': request.get('size', ''),
        'telephoneNumber': request['telephoneNumber'],
        'userId': str(uuid.uuid4()),
    }

    # Putting a try/catch to log to user when some error occurs
    try:
        USERS_TABLE.put_item(
            Item=user_data
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Successfully user created!')
        }
    except Exception as e:
        logging.error("Error creating user:")
        print("Error creating user:")
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps('Error creating the user')
        }


def getuser(document_number):
    response = USERS_TABLE.query(
        IndexName='documentNumberIndex',
        KeyConditionExpression=Key('documentNumber').eq(document_number)
    )
    print('[QUERY RESPONSE]:', response)
    for item in response['Items']:
        if document_number in item:
            logging.error("User already exist")
            raise Exception('User already exist.')
        return True


def convert_to_unix(date):
    if date != '':
        return int(datetime.datetime.strptime(date, "%d/%m/%Y").timestamp())
    return ''


def validate_fields(request, required_fields):
    for key in required_fields:
        if key not in request:
            logging.error("Validation Failed, the following items are required", key)
            raise Exception("Couldn't create the user.")
        return
