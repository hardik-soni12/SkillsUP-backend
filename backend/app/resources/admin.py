from flask import Blueprint
from ..models.user import User
from flask_restful import Api, Resource
from ..schemas.admin_schema import AdminSchema
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity

admin_bp = Blueprint('admin_bp', __name__, '/admin')
admin_api = Api(admin_bp)

admin_schema = AdminSchema(many=True)

# admin required decorater for our admin routes
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        # get the user id from token
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        # checks whether the user exists and are they admin
        if not user or not user.is_admin:
            return {'error':'Admins only!'}, 403
        
        return fn(*args, **kwargs)
    return wrapper



class Admin_UserList(Resource):
    method_decorators = [admin_required]

    def get(self):
        # only admin can see sensitive data(except user password)
        users = User.query.all()
        return admin_schema.dump(users), 200
    
admin_api.add_resource(Admin_UserList, '/users')