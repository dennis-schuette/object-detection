
#### AP accepts filename of image
## fetch image from dropbox
## extract labels from image
#### send labels back


#######################################

from flask import Flask  #, jsonify, request
from flask_restful import Resource, Api, reqparse
from app.model import *
#import pandas as pd
import werkzeug

app = Flask(__name__)
api = Api(app)

#### startup model


@app.route('/')
def home_view():
    return "<h1>model ready</h1>"

# class trigger(Resource):
#     def get(self):
#         #data = pd.read_csv('users.csv')
#         data = {'test': 'hello-world'}
#         return {'data': data}, 200

#     def post(self):
#         parser = reqparse.RequestParser()  # initialize
        
#         parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')  # add args
#         args = parser.parse_args()  # parse arguments to dictionary

#         image_file = args['file']
#         print(image_file)
#         #image_file.save("your_file_name.jpg")

#         return {'data received': image_file}, 200


class UploadImage(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        image_file = args['file']
        image_file.save("tmp.jpeg")
        img, res = detect_img('tmp', img_suffix='jpeg')
        res['score'] = np_to_float(res)
        print(res)
        return {'data': res}, 200

    

api.add_resource(UploadImage, '/')


# https://www.youtube.com/watch?v=s_ht4AKnWZg