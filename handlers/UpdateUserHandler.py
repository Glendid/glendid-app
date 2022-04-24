import boto3
import json
import os

def updateUser(event, context):

    data = json.loads(event['body'])
    if 'userId' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the user item.")
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
                ":o": data['occupation'],
                ":d": data['admissionDate'],
                ":b": data['birthDate'],
                ":c": data['documentType'],
                ":l": data['lastName'],
                ":e": data['created'],
                ":r": data['address'],
                ":m": data['email'],
                ":t": data['telephoneNumber'],
                ":f": data['firstName'],
                ":p": data['role'],
                ":g": data['assigned'],
                ":n": data['documentNumber'],
                ":i": data['description'],
            },
            UpdateExpression= "set active = :a, occupation= :o, admissionDate= :d, birthDate= :b, documentType= :c, lastName= :l, created= :e, address= :r, email= :m, telephoneNumber=:t, firstName= :f, role= :p, assigned= :g, documentNumber= :n, description= :i ",
            ReturnValues="UPDATED_NEW",
        )
        # create a response
        return {
            'statusCode': 200,
            'body': json.dumps('ok user updated')
        }

    except:
        print('Closing lambda function')
        return {
            'statusCode': 400,
            'body': json.dumps("Error updating user")
        }