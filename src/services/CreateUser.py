from src.commons.commons import convert_to_unix
import boto3
import json
import logging
import os
import time
import uuid

dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
USERS_TABLE = dynamodb.Table(os.environ['USERS_TABLE'])


def create_user_service(request):
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

    try:
        response = USERS_TABLE.put_item(
            Item=user_data
        )
        print('[GET RESPONSE]:', response)
        return {
            'statusCode': 200,
            'body': json.dumps('User created.')
        }
    except Exception as e:
        logging.error("Error creating user:")
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps('Error creating the user')
        }
