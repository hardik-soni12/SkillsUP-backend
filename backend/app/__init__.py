from flask import Flask, jsonify
from .extensions import db, ma, bcrypt, jwt, api, migrate
from config import Config_dict
from .resources.auth import auth_bp
from .resources.user_route import user_bp
from .resources.admin import admin_bp
from .resources.skill_route import skill_bp
from .resources.matching_suggestions import match_suggestion_bp
from .resources.match_route import match_bp
from .resources.message_route import message_bp

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(Config_dict[config_name])

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(skill_bp, url_prefix='/users')
    app.register_blueprint(match_suggestion_bp, url_prefix='/matches')
    app.register_blueprint(match_bp, url_prefix='/matches')
    app.register_blueprint(message_bp, url_prefix='/matches')

    return app