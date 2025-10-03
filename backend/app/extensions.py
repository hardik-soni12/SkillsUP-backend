from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_migrate import Migrate


db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
ma = Marshmallow()
api = Api()
migrate = Migrate()