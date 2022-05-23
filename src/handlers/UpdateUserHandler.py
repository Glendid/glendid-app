from boto3.dynamodb.conditions import Key
from src.commons.commons import get_request
from src.services.UpdateUser import update_user_service
import datetime
import boto3
import json
import os
import time

dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
USERS_TABLE = dynamodb.Table(os.environ['USERS_TABLE'])


def update_user(event, context):
    print('[INPUT UPDATE]:', event)
    request = get_request(event)
    return update_user_service(request, event)

