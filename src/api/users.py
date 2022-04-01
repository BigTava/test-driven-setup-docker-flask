from flask import Blueprint, request
from flask_restx import Resource, Api, fields

from src import db
from src.api.models import User

users_blueprint = Blueprint('users', __name__)
api = Api(users_blueprint)

# Here, we used the api.model() factory pattern to instantiate and register 
#the user model to our API. We then defined the type of each field and passed in some optional arguments.
user = api.model('User', {
    'id': fields.Integer(readOnly=True),
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'created_date': fields.DateTime,
})

class UsersList(Resource):
    
    # With that, we can use the @api.expect decorator to 
    #attach the model to the post method in order to validate the payload
    @api.expect(user, validate=True)
    def post(self):
        post_data = request.get_json()
        username = post_data.get('username')
        email = post_data.get('email')
        response_object = {}

        user = User.query.filter_by(email=email).first()
        if user:
            response_object['message'] = 'Sorry. That email already exists.'
            return response_object, 400

        db.session.add(User(username=username, email=email))
        db.session.commit()

        response_object['message'] = f'{email} was added!'
        return response_object, 201

    # The as_list=True argument indicates that we want to return a list of objects rather than a single object
    @api.marshal_with(user, as_list=True)
    def get(self):
        return User.query.all(), 200


class Users(Resource):

    # We used the @api.marshal_with() decorator here and passed in the user model. 
    #This model is now being used as a serializer to generate a JSON object with the fields from the model.
    @api.marshal_with(user)
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            api.abort(404, f"User {user_id} does not exist")
        return user, 200


api.add_resource(UsersList, '/users')
api.add_resource(Users, '/users/<int:user_id>')