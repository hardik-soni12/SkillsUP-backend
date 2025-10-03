from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Api, Resource
from ..extensions import db
from ..models.match import Match
from ..models.user import User
from ..models.skill import Skill
from ..schemas.user_schema import PublicUserSchema

match_suggestion_bp = Blueprint('match_suggestion_bp', __name__, url_prefix='/matches')
match_api = Api(match_suggestion_bp)

public_users_schema = PublicUserSchema(many=True)

# match suggestion 
class MatchSuggestion(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        # get the current user skill
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        # Create simple lists of the names of the skills
        skill_user_knows = {skill.name.lower() for skill in current_user.skills if skill.skill_type == 'knows'}
        skill_user_wants = {skill.name.lower() for skill in current_user.skills if skill.skill_type == 'wants'}

        #  If the user hasn't added any skills, we can't find matches.
        if not skill_user_knows or not skill_user_wants:
            return {"message": "Please add skills you know and want to learn to get matches."}, 400
        
        # find all other users
        # list of every potential user to compare against. exclude the current user from this list
        potential_partners = User.query.filter(User.id != current_user_id).all()

        # matching algorithm
        good_matches = []
        for partner in potential_partners:
            partner_skill_knows = {skill.name.lower() for skill in partner.skills if skill.skill_type == 'knows'}
            partner_skill_wants = {skill.name.lower() for skill in partner.skills if skill.skill_type == 'wants'}

            # - Do any of my 'wants' overlap with their 'knows'?
            # - AND do any of their 'wants' overlap with my 'knows'?
            i_can_teach_them = skill_user_knows.intersection(partner_skill_wants)
            they_can_teach_me = partner_skill_knows.intersection(skill_user_wants)

            if i_can_teach_them and they_can_teach_me:
                # we found a match
                # We'll add the user and the specific matching skills to our results.
                match_data = {
                    'user':public_users_schema.dump([partner])[0],
                    'matching_skills':{
                        'you_can_teach': list(i_can_teach_them),
                        'they_can_teach': list(they_can_teach_me)
                    }
                }
                good_matches.append(match_data)

        return good_matches, 200

match_api.add_resource(MatchSuggestion, '/suggestions')