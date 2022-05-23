from boto3.dynamodb.conditions import Key
from src.commons.commons import DecimalEncoder
import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
USERS_TABLE = dynamodb.Table(os.environ['USERS_TABLE'])


def get_users_service(request):
    load_secondary_index(USERS_TABLE)
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


def load_secondary_index(table):
    while True:
        if not table.global_secondary_indexes or table.global_secondary_indexes[0]['IndexStatus'] != 'ACTIVE':
            print('Waiting for index to backfill...')
            table.sleep(5)
            table.reload()
        else:
            break
