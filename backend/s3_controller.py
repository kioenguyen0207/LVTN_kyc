from boto3 import resource
import cv2
import os
from dotenv import load_dotenv
import urllib.request, json
import ssl
import face_recognition

load_dotenv()
ssl._create_default_https_context = ssl._create_unverified_context
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.getenv('REGION_NAME')
ACCESS_POINT = os.getenv('ACCESS_POINT')

def s3_upload(image, imageName, original=False):
  s3 = resource(
    's3',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME
  )
  try:
    image_string = cv2.imencode('.png', image)[1].tostring()
    if original == False:
      result = s3.Bucket('triip').put_object(Key = imageName, Body=image_string)
    else:
      result = s3.Bucket('triiporiginal').put_object(Key = imageName, Body=image_string)
    print('upload success: \n', result)
  except Exception as ex:
    print('upload failed: \n', ex)
  
def upload_vector_s3(key, value):
  s3 = resource(
    's3',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME
  )
  data = {
    'key': key,
    'value': value
  }
  print('DATA: ----------')
  try:
    result = s3.Bucket('triip').put_object(Key = 'vector.json', Body=(bytes(json.dumps(data).encode('UTF-8'))))
    print('upload success: \n', result)
  except Exception as ex:
    print('upload failed: \n', ex)  

def get_vector_s3():
  with urllib.request.urlopen(ACCESS_POINT + "vector.json") as url:
    data = json.load(url)
    print(data)
    return data

def import_vector_s3(key, value):
  try:
    data = get_vector_s3()
    data['key'].append(key)
    data['value'].append(value.tolist())
    return upload_vector_s3(data['key'], data['value'])
  except Exception as ex:
    print('Error: ' + ex)

def import_image_s3(key, image):
  img = face_recognition.face_encodings(image)[0]
  return import_vector_s3(key, img)
  
if __name__ == '__main__':
  pass
  # reset vector.json
  # print(upload_vector_s3([],[]))