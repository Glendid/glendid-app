from decimal import Decimal
from boto3.dynamodb.conditions import Key
import boto3
import json
import os

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

def get_users(event, context):
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')
    USERS_TABLE = dynamodb.Table(os.environ['USERS_TABLE'])

    request = get_request(event)
    validate_fields(request)
    load_secondary_index(USERS_TABLE)

    # Putting a try/catch to log to user when some error occurs
    try:
        response = USERS_TABLE.query(
            IndexName='roleIndex',
            KeyConditionExpression=Key('role').eq(request['role']),
        )
        print('[GET RESPONSE]:', response)
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'], cls=DecimalEncoder)
        }


    except Exception as e:
        print("Error getting users:")
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps('Error getting users')
        }


def validate_fields(request):
    required_fields = ['role']

    for key in request:
        if required_fields.count(key):
            return request
        raise Exception(key, ' is required')


def load_secondary_index(table):
    while True:
        if not table.global_secondary_indexes or table.global_secondary_indexes[0]['IndexStatus'] != 'ACTIVE':
            print('Waiting for index to backfill...')
            table.sleep(5)
            table.reload()
        else:
            break


def get_request(event):
    print('[INPUT]:', event)
    body = event['body']
    set_request = json.loads(body)
    return set_request
