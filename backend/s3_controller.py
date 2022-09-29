from boto3 import resource
import cv2
import os
from dotenv import load_dotenv

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.getenv('REGION_NAME')

def s3_upload(image, imageName):
  s3 = resource(
    's3',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME
  )
  try:
    image_string = cv2.imencode('.png', image)[1].tostring()
    result = s3.Bucket('triip').put_object(Key = imageName, Body=image_string)
    print('upload success: \n', result)
  except Exception as ex:
    print('upload failed: \n', ex)

  