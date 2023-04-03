import json
import uuid
from datetime import datetime, timedelta, timezone

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required, unset_jwt_cookies
from werkzeug.security import check_password_hash, generate_password_hash

from api.query import *

auth_bp = Blueprint('api', __name__)

@auth_bp.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()['exp']
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(hours=12))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data['access_token'] = access_token
                response.data = json.dumps(data)
            return response
    except(RuntimeError, KeyError):
        return response

@auth_bp.route('/api/auth/login', methods=['GET', 'POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        return {"message": "Wrong username or password"}, 401
    
    try:
        row = check_user(username).fetchall()[0]
    except:
        # row = check_user(username).fetchall()[0]
        return {"message": "Wrong username or password"}, 401
    
    if check_password_hash(row['KataSandi'], password):
        access_token = create_access_token(identity=row['NoRec'])

    return {
        "access_token": access_token,
        "current_user": {
            "username": row['NamaUserMobile'],
            "email": row['NamaUserEmail'],
            "fullname": row['NamaLengkap'],
            "birth_date": row['TglLahir'],
            "gender": row['KdJenisKelamin'],
            "indentity": row['NoIdentitas'],
            "address": row['AlamatLengkap'],
        }
    }

@auth_bp.route('/auth/logout', methods=['GET'])
def logout():
    response = jsonify({"message": "logout successful"})
    unset_jwt_cookies(response)
    return response

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    username = request.json.get("username", None)
    fullname = request.json.get("fullname", None).title()
    email = request.json.get("email", None)
    password = generate_password_hash(request.json.get("password", None), method='sha1', salt_length=4)

    user_id = get_id().scalar() + 1
    register_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    profile_id = 1
    status_enable = 1
    rec_no = str(uuid.uuid4())

    if not username or not fullname or not email or not password:
        return {'status': "field can't blank"}, 403
    else:
        try:
            row = check_user(username).fetchall()[0]
            return {'status': "username already used"}, 403
        except:
            create_user(user_id, username, fullname, email, password, register_date, profile_id, status_enable, rec_no)
            return {'status': 'new user created'}
        
