from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr
import os
from dotenv import load_dotenv
from datetime import datetime
import random

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.getenv('REGION_NAME')

resource = resource(
   'dynamodb',
   aws_access_key_id     = AWS_ACCESS_KEY_ID,
   aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
   region_name           = REGION_NAME
)

kyc_requests_table = resource.Table('kyc_requests')

def importData(user_id, username, address, phone, image_path, detected_objects, time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")):
    response = kyc_requests_table.put_item(
        Item = {
            'request_id': random.randint(100000, 999999),
            'user_id': user_id,
            'username': username,
            'address' : address,
            'phone'  : phone,
            'createdAt': time,
            'updatedAt': time,
            'image': image_path,
            'detected_objects': detected_objects,
            'comment': 'null',
            'approver': 'admin',
            'kycStatus': 'pending'
        }
    )
    print(response)
    return response

def readPendingReq():
    response = kyc_requests_table.scan(
        FilterExpression = Attr("kycStatus").eq('pending')
    )
    return response['Items']

def readAllReq():
    response = kyc_requests_table.scan()
    return response['Items']

def readRejectedReq():
    response = kyc_requests_table.scan(
        FilterExpression = Attr("kycStatus").eq('rejected')
    )
    return response['Items']

def readApprovedReq():
    response = kyc_requests_table.scan(
        FilterExpression = Attr("kycStatus").eq('approved')
    )
    return response['Items']

def readById(id):
    response = kyc_requests_table.query(
        KeyConditionExpression=Key('request_id').eq(id)
    )
    return response['Items']

if __name__ == '__main__':
    # for item in readAllReq():
    #     print('------')
    #     print(item)

    print(readById(69))