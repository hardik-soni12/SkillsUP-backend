from flask import request, Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.user import User
from ..models.match import Match
from ..models.skill import Skill
from ..schemas.match_schema import MatchSchema
from sqlalchemy import or_, and_

match_bp = Blueprint('match_bp', __name__, url_prefix='/matches')
match_api = Api(match_bp)

match_schema = MatchSchema()
matches_schema = MatchSchema(many=True)

class MatchListResource(Resource):
    method_decorators={'get':[jwt_required()], 'post':[jwt_required()]}
    def get(self):
        # Get all the connections of the current logged_in user
        current_user_id = get_jwt_identity()
        
        # This query finds all matches where the current user is either user1 OR user2
        user_matches = Match.query.filter(or_(Match.user1_id == current_user_id, Match.user2_id == current_user_id)).all()

        return matches_schema.dump(user_matches), 200
    
    def post(self):
        # create a new match request
        current_user_id = get_jwt_identity()
        data = request.get_json() or {}

        user2_id = data.get('user2_id')
        if not user2_id:
            return {"error": "user2_id is required."}, 400
        
        # prevent users from matching with themselves
        if int(current_user_id) == int(user2_id):
            return {'error': 'You cannot match with yourself'}, 400
        
        # check if connection already exists to prevent duplicates(in any order)
        existing_match = Match.query.filter(or_(
            and_(Match.user1_id == current_user_id, Match.user2_id == user2_id),
            and_(Match.user1_id == user2_id, Match.user2_id == current_user_id)
            )).first()
        
        if existing_match:
            return {"error": "A match or pending request with this user already exists."}, 400
        
        # create a Match with pending status
        new_match = Match(
            user1_id = current_user_id, #The sender of the request
            user2_id = user2_id #The reciever of the request
        )

        db.session.add(new_match)
        db.session.commit()

        return match_schema.dump(new_match), 201
    

class MatchResource(Resource):
    method_decorators={'put':[jwt_required()], 'delete':[jwt_required()]}
    
    def put(self, match_id):
        # Accept or Reject a pending match request
        current_user_id = get_jwt_identity()
        match = Match.query.get_or_404(match_id)

        # Only the receiver of the request (user2) can accept or reject it
        if int(match.user2_id) != int(current_user_id):
            return {'error': 'Unauthorized. You can only respond to match requests sent to you.'}, 403
        
        if match.status != 'pending':
            return {'error': f'This match is already "{match.status}" and cannot be changed.'}, 400
        
        data = request.get_json() or {}
        new_status = data.get('status')

        if new_status not in ['accepted', 'rejected']:
            return {"error": "Invalid Status. Must be 'accepted' or 'rejected'."}, 400
        
        match.status = new_status
        db.session.commit()

        return match_schema.dump(match), 200
    

    def delete(self, match_id):
        # Cancel a pending request or unmatch with a user
        current_user_id = get_jwt_identity()
        match = Match.query.get_or_404(match_id)

        # you must be one of the two person in the match to delete
        if int(current_user_id) not in [int(match.user1_id), int(match.user2_id)]:
            return {"error": "Unauthorized. You cannot delete a match you are not a part of."}, 403

        db.session.delete(match)
        db.session.commit()

        return {"message": "Match deleted successfully."}, 200


match_api.add_resource(MatchListResource, '')
match_api.add_resource(MatchResource, '/<int:match_id>')