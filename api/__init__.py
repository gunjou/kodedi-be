from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager


api = Flask(__name__)
CORS(api)

api.config['JWT_SECRET_KEY'] = '084143fc-450e-4b3c-9435-a3ba4bca4e61'
api.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=12)
jwt = JWTManager(api)


from api.auth import auth_bp
api.register_blueprint(auth_bp, name='auth')
from api.profile import profile_bp
api.register_blueprint(profile_bp, name='profile')
from api.pasien import pasien_bp
api.register_blueprint(pasien_bp, name='pasien')
from api.master import master_bp
api.register_blueprint(master_bp, name='master')

# if __name__ == "__main__":
#     api.run(ssl_context='adhoc')
