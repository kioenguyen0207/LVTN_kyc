import face_recognition
from urllib.request import urlopen
import json
import numpy as np
from dotenv import load_dotenv
import os
import ssl
import heapq
import operator
ssl._create_default_https_context = ssl._create_unverified_context

load_dotenv()
ACCESS_POINT = os.getenv('ACCESS_POINT')

def get_n_most_similar_face(distance_list, key_list):
  try:
    smallest_index = list(zip(*heapq.nsmallest(5, enumerate(distance_list), key=operator.itemgetter(1))))[0]
  except:
    smallest_index = []
  result = []
  for index in smallest_index:
    result.append(key_list[index])
  return result

def get_most_similar_image(image):
  # load phase
  response = urlopen(ACCESS_POINT + 'vector.json')
  data_json = json.loads(response.read())
  data_key = data_json['key']
  data_value = data_json['value']
  # convert list to its original form
  # converted_value = np.array(data_value, dtype=np.ndarray)
  converted_list = []
  for element in data_value:
    converted_list.append(np.array(element))
  loaded_img = face_recognition.load_image_file(image)
  encodedImg = face_recognition.face_encodings(loaded_img)[0]
  distance = face_recognition.face_distance(data_value, encodedImg)
  result = get_n_most_similar_face(distance, data_key)
  return result

if __name__ == '__main__':
  get_most_similar_image()