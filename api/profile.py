from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required

from api.query import get_data_user


profile_bp = Blueprint('api', __name__)

@profile_bp.route('/api/users/profile', methods=['GET'])
@jwt_required()
def my_profile():
    current_user = get_data_user(get_jwt_identity()).fetchall()[0]
    print(current_user)
    result = {
            "username": current_user['NamaUserMobile'],
            "email": current_user['NamaUserEmail'],
            "fullname": current_user['NamaLengkap'],
            "birth_date": current_user['TglLahir'],
            "gender": current_user['KdJenisKelamin'],
            "indentity": current_user['NoIdentitas'],
            "address": current_user['AlamatLengkap'],
        }
    return result