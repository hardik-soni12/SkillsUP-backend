from flask import Blueprint, request
from flask_restful import Resource, Api
from ..models.user import User
from ..extensions import db
from ..utils.jwt_utils import generate_tokens, get_current_user_id, refresh_access_token, logout_user
from ..schemas.auth_schema import RegisterSchema, LoginSchema
from ..schemas.user_schema import UserSchema
from flask_jwt_extended import jwt_required


auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')
auth_api = Api(auth_bp)

register_schema = RegisterSchema()
login_schema = LoginSchema()
user_schema = UserSchema()


# registration api route
class Register(Resource):
    def post(self):
        data = request.get_json() or {}

        # validate data with register schema
        errors = register_schema.validate(data)
        if errors:
            return {'errors': errors}, 400
        
        # check if username already exists
        if User.query.filter_by(username=data['username']).first():
            return {'error':'username already taken'}, 400

        # check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return {"error":"email already registered"}, 400
        
        # create new user
        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            bio=data.get('bio')
        )

        db.session.add(user)
        db.session.commit()

        return {
            'msg':'user created successfully',
            'user': user_schema.dump(user)
        }, 201
    

# login api route
class Login(Resource):
    def post(self):
        data = request.get_json() or {}

        # validate data with login schema
        errors = login_schema.validate(data)
        if errors:
            return {'errors': errors}, 400
        
        # check if user exists and password matches
        user = User.query.filter_by(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            return {'error': 'Invalid credentials'}, 401
        
        # generate token using util functions
        tokens = generate_tokens(user.id)

        user_data = user_schema.dump(user)

        return {
            'access_token': tokens['access_token'],
            'refresh_token': tokens['refresh_token'],
            'user': user_data
        }, 200
    

# get current user
class Me(Resource):
    @jwt_required()
    def get(self):
        # get details of the logged-in user
        user_id = get_current_user_id()
        user = User.query.get(user_id)
        if not user:
            return {'error': 'user not found'}, 404
        return user_schema.dump(user), 200
    

# refresh access token
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        return refresh_access_token()
    

# logout api route
class Logout(Resource):
    def post(self):
        # logout and clear jwt tokens
        return logout_user()
    

auth_api.add_resource(Register, '/register')
auth_api.add_resource(Login, '/login')
auth_api.add_resource(Me, '/me')
auth_api.add_resource(Refresh, '/refresh')
auth_api.add_resource(Logout, '/logout')