from datetime import datetime
import Enums
import boto3
import json
import os
import uuid

client = boto3.client('dynamodb')

def createUser(event, context):

    # Instanciating connection objects with DynamoDB using boto3 dependency
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')

    # Getting the table users
    USERS_TABLE = dynamodb.Table(os.environ['USERS_TABLE'])

    body = event['body']
    request = json.loads(body)

    # Getting the data from request
    address = request['address']
    admissionDate = request['admissionDate']
    assigned = request['assigned']
    birthDate = request['birthDate']
    description = request['description']
    documentNumber = request['documentNumber']
    documentType = request['documentType']
    email = request['email']
    firstName = request['firstName']
    lastName = request['lastName']
    occupation = request['occupation']
    role = request['role']
    telephoneNumber = request['telephoneNumber']

    userData: object = {
                'active': True,
                'address': address,
                'admissionDate': admissionDate,
                'assigned': assigned,
                'birthDate': birthDate,
                'created': (datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
                'description': description,
                'documentNumber': documentNumber,
                'documentType': documentType,
                'email': email,
                'firstName': firstName,
                'lastName': lastName,
                'occupation': occupation,
                'role': role,
                'telephoneNumber': telephoneNumber,
                'userId': str(uuid.uuid4()),
            }

    # Putting a try/catch to log to user when some error occurs
    try:
        USERS_TABLE.put_item(
            Item = userData
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Succesfully user created!')
        }
    except:
        print('Closing lambda function')
        return {
            'statusCode': 400,
            'body': json.dumps('Error saving the user')
        }