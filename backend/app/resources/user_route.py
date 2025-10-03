from flask import request, Blueprint
from ..extensions import db
from ..models.user import User
from ..models.skill import Skill
from  ..schemas.user_schema import UserSchema, PublicUserSchema
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user_bp',__name__,url_prefix='/users')
user_api = Api(user_bp)

user_schema = UserSchema()
public_user_schema = PublicUserSchema()
public_users_schema = PublicUserSchema(many=True)

# user profile api route(user id)
class UserProfile(Resource):
    # best way to apply jwt_required decorator on methods to avoid TypeError:unexpected keyword argument 'id'
    method_decorators = {
        'put':[jwt_required()],
        'delete':[jwt_required()]
        }
        

    def get(self, id):
        user = User.query.get_or_404(id) #User profile Id 
        return public_user_schema.dump(user), 200
    
    
    def put(self, id):
        # update logged-in users profile
        current_user_id = get_jwt_identity()


        if int(current_user_id) != id:
            return {"error": "Unauthorized"}, 403
        
        data = request.get_json() or {}
        user = User.query.get_or_404(id)

        if 'username' in data:
            user.username = data['username']
        if 'bio' in data:
            user.bio = data['bio']

        db.session.commit()
        return user_schema.dump(user), 200
    
    
    def delete(self, id):
        # delete logged In users profile
        current_user_id = get_jwt_identity()
        if int(current_user_id) != id:
            return {"error": "Unauthorized"}, 403
        
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {'msg':'User deleted successfully'}, 200
    

# Users list api route 
class UserList(Resource):
    def get(self):
        # Get all users, with optional filtering by skill
        # get the query parameters from the URL
        skill_name = request.args.get('skill_name')
        skill_type = request.args.get('skill_type')

        # base query for all users
        query = User.query

        # If filters are provided, modify the query.
        if skill_name and skill_type:
            # join the User table with the Skill table.
            # This allows us to search for users based on the properties of their skills.
            query = query.join(Skill).filter(
                # Using .ilike() for a case-insensitive search
                Skill.name.ilike(f"%{skill_name}%"),
                Skill.skill_type == skill_type
            )

        users = query.all()
        return public_users_schema.dump(users), 200
    

user_api.add_resource(UserProfile, "/<int:id>")
user_api.add_resource(UserList, "")