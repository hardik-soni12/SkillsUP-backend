from flask import request, Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.match import Match
from ..models.message import Message
from ..schemas.messge_schema import MessageSchema

message_bp = Blueprint('message_bp', __name__, url_prefix='/matches')
message_api = Api(message_bp)

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

class MessageResource(Resource):
    method_decorators={'post':[jwt_required()], 'get':[jwt_required()]}

    def get(self, match_id):
        # Get the full conversation history for a specific match
        current_user_id = get_jwt_identity()
        match = Match.query.get_or_404(match_id)

        if int(current_user_id) not in [int(match.user1_id), int(match.user2_id)]:
            return {"error": "Unauthorized. You cannot view messages for a match you are not in."}, 403
        
        # return all message associated with the match, order by timestamp
        messages = Message.query.filter_by(match_id=match_id).order_by(Message.timestamp.asc()).all()
        return messages_schema.dump(messages), 200
    
    def post(self, match_id):
        # send a message in a specific match
        current_user_id = get_jwt_identity()
        match = Match.query.get_or_404(match_id)

        if int(current_user_id) not in [int(match.user1_id), int(match.user2_id)]:
            return {'error': 'Unauthorized. You cannot view messages for a match you are not in.'}, 403
        
        # You can only send messages in an 'accepted' match
        if match.status != 'accepted':
            return {'error': f"You cannot send messages in a match with status '{match.status}'."}, 400
        
        data = request.get_json() or {}
        text = data.get('text')

        # valdation: message txt cannot be empty
        if not text:
            return {'error': 'Message text is required'}, 400
        
        # create a new message objct 
        new_message = Message(
            text=text,
            match_id=match_id,
            sender_id=current_user_id
        )

        db.session.add(new_message)
        db.session.commit()

        return message_schema.dump(new_message), 201
    
message_api.add_resource(MessageResource, '/<int:match_id>/messages')