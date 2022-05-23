from decimal import Decimal
import datetime
import json
import logging


def get_request(event):
    body = event['body']
    set_request = json.loads(body)
    return set_request


def validate_fields(request, required_fields):
    for key in required_fields:
        if key not in request:
            logging.error("Validation Failed, the following items are required", key)
            raise Exception("Couldn't create the user.")
        return


def convert_to_unix(date):
    if date != '':
        return int(datetime.datetime.strptime(date, "%d/%m/%Y").timestamp())
    return ''


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

