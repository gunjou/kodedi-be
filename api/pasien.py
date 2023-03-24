from datetime import date
import uuid
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from api.query import get_list_patient, query_add_pasien, get_no_cm


pasien_bp = Blueprint('api', __name__)

def get_age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

@pasien_bp.route('/pasien/list', methods=['GET'])
@jwt_required()
def list_pasien():
    data = get_list_patient()
    result = [
        {
            'no_cm': i['NoCM'],
            'fullname': i['NamaLengkap'],
            'gender': 'L' if i['KdJenisKelamin'] == 1 else 'P',
            'age': get_age(i['TglLahir']),
            'status': i['StatusEnabled'],
        } for i in data]
    return result

@pasien_bp.route('/pasien/count', methods=['GET'])
@jwt_required()
def count_pasien():
    patients = get_list_patient().fetchall()
    patients = [i['KdJenisKelamin'] for i in patients]
    result = {
        'laki-laki': patients.count(1),
        'perempuan': patients.count(2),
        'total': len(patients),
    }
    return result

@pasien_bp.route('/pasien/status', methods=['GET'])
@jwt_required()
def count_status():
    patients = get_list_patient().fetchall()
    patients = [i['StatusEnabled'] for i in patients]
    result = {
        'antri': patients.count(1),
        'proses': patients.count(2),
        'selesai': patients.count(3),
        'batal': patients.count(0),
    }
    return result

@pasien_bp.route('/pasien/tambah', methods=['GET', 'POST'])
@jwt_required()
def add_pasien():
    title = request.json.get("title", None)
    fullname = request.json.get("fullname", None).title()
    gender = request.json.get("gender", None)
    nationality = request.json.get("nationality", None)
    birth_date = request.json.get("birth_date", None)

    no_cm_tmp = get_no_cm().fetchall()[-1]
    no_cm = str(int(no_cm_tmp['NoCM']) + 1).zfill(15)
    tmp_name = fullname.split(' ')
    familyname = tmp_name[-1]
    surename = tmp_name[0]
    frontname = tmp_name[0]
    middlename = tmp_name[1]
    backname = tmp_name[-1]
    profile = 1
    status = 1
    no_verifikasi = 1 #date.today().strftime('%y%m%d')
    no_rec = uuid.uuid4()
    
    if not title or not fullname or not gender or not nationality or not birth_date:
        return {'status': "field can't blank"}, 403
    else:
        query_add_pasien(
            profile,
            no_cm,
            title,
            fullname,
            familyname,
            surename,
            frontname,
            middlename,
            backname,
            gender,
            birth_date,
            nationality,
            status,
            no_verifikasi,
            no_rec)
        return {'status': "Success add patient"}
