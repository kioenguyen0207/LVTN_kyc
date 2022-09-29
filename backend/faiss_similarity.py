import cv2
from triip_detect import detect
import numpy as np

def getHashedFace(image_path):
  image = cv2.imread(image_path)
  result = detect(image)
  for label, value in result.items():
    if isinstance(value, list) and label == 'real_face':
      croppedFace = image[value[1]:value[3], value[0]:value[2]]
  cv2.imshow('window', croppedFace)
  cv2.waitKey(0)
  cv2.destroyAllWindows() 


if __name__ == '__main__':
  getHashedFace('inference/images/minhhon.png')
  