from src.commons.commons import convert_to_unix
import boto3
import json
import logging
import os
import time

dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
USERS_TABLE = dynamodb.Table(os.environ['USERS_TABLE'])


def update_user_service(request, event):
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
        logging.error("Error updating user:")
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps('Error updating the user')
        }