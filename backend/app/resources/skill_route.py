from flask import request, Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.skill import Skill
from ..models.user import User
from ..extensions import db
from ..schemas.skill_schema import SkillSchema

skill_bp = Blueprint('skill_bp', __name__, url_prefix='/users')
skill_api = Api(skill_bp)

skill_schema = SkillSchema()
skills_schema = SkillSchema(many=True)

# skills list
class SkillListResource(Resource):

    method_decorators={
        'post':[jwt_required()]}

    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        # going to use the 'skills' relationship on the User model directly.
        return skills_schema.dump(user.skills), 200
    
    def post(self, user_id):
        # add a new skill to users profile
        current_user_id = get_jwt_identity()
        if int(current_user_id) != user_id:
            return {'error':'Unauthorized'}, 403
        
        # get and validate data
        data = request.get_json() or {}
        errors = skill_schema.validate(data, session=db.session)
        if errors:
            return {'errors':errors}, 400

        # check for required fields manually
        if not data.get('name') or not data.get('skill_type'):
            return {'error':'name and skill_type are required fields'}, 400
        
        # create new skill object
        new_skill = Skill(
            name=data['name'],
            skill_type=data['skill_type'],
            user_id=user_id
        )

        db.session.add(new_skill)
        db.session.commit()

        return skill_schema.dump(new_skill), 201
    
# This resource will be mapped to /users/<int:user_id>/skills/<int:skill_id>
class SkillsResource(Resource):
    method_decorators={
        'put':[jwt_required()],
        'delete':[jwt_required()]
    }

    def put(self, user_id, skill_id):
        current_user_id = get_jwt_identity()
        if int(current_user_id) != user_id:
            return {'error':'Unauthorized'}, 403
        
        # Find the specific skill to update
        # ensures the skill belongs to the correct user
        skill = Skill.query.filter_by(id=skill_id, user_id=user_id).first_or_404()
        
        data = request.get_json() or {}

        # Update the skill object with the new data.
        skill.name = data.get('name', skill.name)
        skill.skill_type = data.get('skill_type', skill.skill_type)

        db.session.commit()
        return skill_schema.dump(skill), 200
    
    def delete(self, user_id, skill_id):
        current_user_id = get_jwt_identity()
        if int(current_user_id) != user_id:
            return {'error':'Unauthorized'}, 403
        
        skill = Skill.query.filter_by(id=skill_id, user_id=user_id).first_or_404()

        db.session.delete(skill)
        db.session.commit()

        return {'message':'Skill deleted successfully'}, 200

    
skill_api.add_resource(SkillListResource, '/<int:user_id>/skills')
skill_api.add_resource(SkillsResource, '/<int:user_id>/skills/<int:skill_id>')