from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr
import os
from dotenv import load_dotenv
from datetime import datetime
from s3_controller import import_image_s3
import requests
from io import BytesIO
import cv2
import numpy as np

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.getenv('REGION_NAME')
ACCESS_POINT = os.getenv('ACCESS_POINT')

resource = resource(
   'dynamodb',
   aws_access_key_id     = AWS_ACCESS_KEY_ID,
   aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
   region_name           = REGION_NAME
)

kyc_requests_table = resource.Table('kyc_requests1')

def importData(user_id, username, address, phone, image_path, detected_objects, similar_faces = [], time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")):
    response = kyc_requests_table.put_item(
        Item = {
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
            'kycStatus': 'pending',
            'similar_faces': similar_faces
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

def readByUserId(id):
    response = kyc_requests_table.query(
        KeyConditionExpression=Key('user_id').eq(id)
    )
    return response['Items']

def updateKycStatus(id, status):
    response = kyc_requests_table.update_item(
        Key = {
            'user_id': id
        },
        AttributeUpdates = {
            'kycStatus': {
                'Value'  : status,
                'Action' : 'PUT'
            }
        },
        ReturnValues = "UPDATED_NEW"
    )
    if status == 'approved':
        response2 = requests.get(ACCESS_POINT + id + '.png')
        import_image_s3(ACCESS_POINT + id + '.png', cv2.imdecode(np.frombuffer(response2.content, np.uint8), cv2.IMREAD_COLOR))
    return response
 
if __name__ == '__main__':
    for item in readAllReq():
        print('------')
        print(item)