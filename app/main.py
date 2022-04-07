
#### AP accepts filename of image
## fetch image from dropbox
## extract labels from image
#### send labels back


#######################################

from flask import Flask
from flask_restful import Resource, Api, reqparse
#import pandas as pd

app = Flask(__name__)
#api = Api(app)

@app.route('/')
def home_view():
    return "<h1>Home view</h1>"


#class Users(Resource):
    ### post request
    # def post(self):
    #     parser = reqparse.RequestParser()  # initialize
        
    #     parser.add_argument('userId', required=True)  # add args
    #     parser.add_argument('name', required=True)
    #     parser.add_argument('city', required=True)
        
    #     args = parser.parse_args()  # parse arguments to dictionary
        
    #     # create new dataframe containing new values
    #     new_data = pd.DataFrame({
    #         'userId': args['userId'],
    #         'name': args['name'],
    #         'city': args['city'],
    #         'locations': [[]]
    #     })
    #     # read our CSV
    #     data = pd.read_csv('users.csv')

    #     if args['userId'] in list(data['userId']):
    #         return {'message': 'user already exists."'}, 401
    #     else:
    #         # add the newly provided values
    #         data = data.append(new_data, ignore_index=True)
    #         # save back to CSV
    #         data.to_csv('users.csv', index=False)

    ### get request
 #   def get(self):
 #       #data = pd.read_csv('users.csv')
 #       data = {'test': 'hello-world'}
 #       return {'data': data}, 200

    

#api.add_resource(Users, '/users')  # '/users' is our entry point for Users


@app.route('/users', methods=['GET'])
def get_function():
    #data = pd.read_csv('users.csv')
    data = {'test': 'hello-flask'}
    return {'data': data}, 200

#if __name__ == '__main__':
#    app.run()  # run our Flask app