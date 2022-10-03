from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
import werkzeug
import cv2
import numpy as np
from triip_detect import detect
import os
from dotenv import load_dotenv
from flask_cors import CORS

from s3_controller import s3_upload
from db_controller import importData, readPendingReq, readAllReq, readRejectedReq, readApprovedReq, readById, readByUserId

app = Flask(__name__)
CORS(app)
api = Api(app)

load_dotenv()
ACCESS_POINT = os.getenv('ACCESS_POINT')

class Home(Resource):
    def get(self):
        try:
            return {'server_status': 'OK'}, 200
        except Exception as ex:
            return {'msg': "Something's happened",
                    'error details': ex}, 500

class send_kyc_request(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser(bundle_errors=True)
            parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', required=True)
            parser.add_argument('user_id', location='form', required=True)
            parser.add_argument('username', location='form', required=True)
            parser.add_argument('address', location='form', required=True)
            parser.add_argument('phone', location='form', required=True)
            args = parser.parse_args()
            uploaded_image = args['file'].read()
            img = cv2.imdecode(np.frombuffer(uploaded_image, np.uint8), cv2.IMREAD_COLOR)
            result = detect(img)
            detectedElements = []
            for key in result:
                p = result[key]
                img = cv2.rectangle(img, (p[0], p[1]) , (p[2], p[3]), (255, 0, 0), 2)
                detectedElements.append(key)
            s3_upload(img, args['user_id'] + '.png')
            importData(args['user_id'], args['username'], args['address'], args['phone'], ACCESS_POINT + args['user_id'] + '.png', detectedElements)
            return {
                'Status': 'Success!'
            }
        except Exception as ex:
            print(ex)
            return {
                'msg': "Something's happened",
                'description': str(ex)
                }, 500

class getAllRequest(Resource):
    def get(self):
        try:
            return jsonify(readAllReq())
        except Exception as ex:
            return {
                'msg': "Something's happened",
                'description': str(ex)
                }, 500

class getRejectedRequest(Resource):
    def get(self):
        try:
            return jsonify(readRejectedReq())
        except Exception as ex:
            return {
                'msg': "Something's happened",
                'description': str(ex)
                }, 500

class getPendingRequest(Resource):
    def get(self):
        try:
            return jsonify(readPendingReq())
        except Exception as ex:
            return {
                'msg': "Something's happened",
                'description': str(ex)
                }, 500

class getApprovedRequest(Resource):
    def get(self):
        try:
            return jsonify(readApprovedReq())
        except Exception as ex:
            return {
                'msg': "Something's happened",
                'description': str(ex)
                }, 500

# class getById(Resource):
#     def get(self):
#         try:
#             id = request.args.get('id')
#             return jsonify(readById(int(id))[0])
#         except Exception as ex:
#             return {
#                 'msg': "Something's happened",
#                 'description': str(ex)
#                 }, 500

class getByUserId(Resource):
    def get(self):
        try:
            id = request.args.get('id')
            return jsonify(readByUserId(id)[0])
        except Exception as ex:
            return {
                'msg': "Something's happened",
                'description': str(ex)
                }, 500

#endpoint(s)
api.add_resource(Home, "/")
api.add_resource(send_kyc_request, "/kyc")
api.add_resource(getAllRequest, "/get/all")
api.add_resource(getRejectedRequest, "/get/rejected")
api.add_resource(getPendingRequest, "/get/pending")
api.add_resource(getApprovedRequest, "/get/approved")
api.add_resource(getByUserId, "/getuser")

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5050)