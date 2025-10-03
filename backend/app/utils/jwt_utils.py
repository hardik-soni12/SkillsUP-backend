from flask import jsonify
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    get_jwt_identity, 
    set_refresh_cookies, 
    unset_jwt_cookies
)

def generate_tokens(user_id):
    access_token = create_access_token(identity=str(user_id))
    refresh_token = create_refresh_token(identity=str(user_id))

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


def get_current_user_id():
    # Shortcut for getting the current logged-in user ID
    return get_jwt_identity()


def refresh_access_token():
    user_id = get_current_user_id()
    if not user_id:
        return {"msg": "User not logged in"}, 401
    else:
        return {"access_token": create_access_token(identity=user_id)}, 200
    

def logout_user():
    resp = jsonify({'msg': 'successfully logged out'})
    unset_jwt_cookies(resp)
    return resp