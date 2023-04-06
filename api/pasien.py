from datetime import date, datetime, timedelta
import time
from dateutil import parser
import uuid
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from api.query import get_list_patient, query_add_pasien, get_no_cm, query_add_komponen_anamnesis, get_master_komponen_anamnesis, get_anamnesis, get_no_periksa, query_add_verifikasi, get_no_verif, get_master_anamnesis


pasien_bp = Blueprint('api', __name__)

def get_age(birthdate):
    today = date.today()
    # age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    ages = today - birthdate
    years = ages.days / 365.242
    months = (years - int(years)) * 12
    days = (months - int(months)) * (365.242/12)
    return f"{int(years)}%{int(months)}%{int(days)}"

def add_verification(no_verifikasi, code):
    profile_id = 1
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    tgl = now[:-3]
    status = 1
    no_rec = uuid.uuid4()
    query_add_verifikasi(profile_id, no_verifikasi, tgl, code, status, no_rec)



@pasien_bp.route('/api/pasien/list', methods=['GET'])
@jwt_required()
def list_pasien():
    data = get_list_patient()
    result = [
        {
            'no_cm': i['NoCM'],
            'fullname': i['NamaLengkap'],
            'gender': 'L' if i['KdJenisKelamin'] == 1 else 'P',
            'age_y': get_age(i['TglLahir']).split('%')[0],
            'age_m': get_age(i['TglLahir']).split('%')[1],
            'age_d': get_age(i['TglLahir']).split('%')[2],
            'status': i['KodeVerifikasi'],
        } for i in data]
    result = sorted(result, key=lambda d: d['no_cm'])
    return result

@pasien_bp.route('/api/pasien/get-detail-patient', methods=['GET'])
@jwt_required()
def get_pasien():
    data = get_list_patient()
    result = [
        {
            'no_cm': i['NoCM'],
            'fullname': i['NamaLengkap'],
            'gender': 'L' if i['KdJenisKelamin'] == 1 else 'P',
            'age_y': get_age(i['TglLahir']).split('%')[0],
            'age_m': get_age(i['TglLahir']).split('%')[1],
            'age_d': get_age(i['TglLahir']).split('%')[2],
            'status': i['KodeVerifikasi'],
        } for i in data]
    return result

@pasien_bp.route('/api/pasien/count', methods=['GET'])
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

@pasien_bp.route('/api/pasien/status', methods=['GET'])
@jwt_required()
def count_status():
    patients = get_list_patient().fetchall()
    patients = [i['KodeVerifikasi'] for i in patients]
    result = {
        'antri': patients.count(1),
        'proses': patients.count(2),
        'selesai': patients.count(3),
        'batal': patients.count(0),
    }
    return result

@pasien_bp.route('/api/pasien/tambah', methods=['GET', 'POST'])
@jwt_required()
def add_pasien():
    title = request.json.get("title", None)
    fullname = request.json.get("fullname", None).title()
    gender = request.json.get("gender", None)
    # nationality = request.json.get("nationality", None)
    birth_date = request.json.get("birth_date", None)

    nationality = 1
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
    no_verif_tmp = get_no_verif(date.today().strftime('%y%m%d')).fetchall()[-1]['NoVerifikasi']
    no_verif_tmp = int(no_verif_tmp[-4:])
    no_verifikasi = date.today().strftime('%y%m%d') + str(no_verif_tmp + 1).zfill(4)
    no_rec = uuid.uuid4()
    
    if not title or not fullname or not gender or not nationality or not birth_date:
        return {'status': "field can't blank"}, 403
    else:
        add_verification(no_verifikasi, 1)
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

@pasien_bp.route('/api/pasien/anamnesis', methods=['POST'])
@jwt_required()
def add_komponen_anamnesis():
    NoCM = request.json.get("patient", None)
    keluhan = request.json.get("keluhan", None)
    tgl_periksa = request.json.get("tgl_periksa", None)
    komponen = get_master_anamnesis()
    komponen = [i['KdKomponen'] for i in komponen]
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    TglHasilPeriksa = now[:-3]#tgl_periksa
    
    StatusEnabled = 1
    KdProfile = 1
    NoHasilPeriksa = 1 #get_no_periksa().fetchall()[-1][0]
    try:
        no_verif_tmp = get_no_verif(date.today().strftime('%y%m%d')).fetchall()[-1]['NoVerifikasi']
    except:
        no_verif_tmp = '0000'
    no_verif_tmp = int(no_verif_tmp[-4:])
    no_verifikasi = date.today().strftime('%y%m%d') + str(no_verif_tmp + 1).zfill(4)

    add_verification(no_verifikasi, 2)
    for i in komponen:
        time.sleep(1)
        NoRec = uuid.uuid4()
        KdKomponenPeriksa = i
        HasilKomponenPeriksa = 0
        for j in keluhan:
            if i == j:
                HasilKomponenPeriksa = 1
        query_add_komponen_anamnesis(KdProfile, NoHasilPeriksa, NoCM, TglHasilPeriksa, StatusEnabled, NoRec, KdKomponenPeriksa, HasilKomponenPeriksa, no_verifikasi)
    
    return {'status': "Success add komponen"}

@pasien_bp.route('/api/pasien/get-anamnesis', methods=['GET', 'POST'])
@jwt_required()
def get_komponen_anamnesis():
    no_cm = request.json.get("patient", None)
    komponen = get_anamnesis(no_cm)
    result = [{'keluhan': i['NamaKomponen'], 'date': i['TglHasilKomponenPeriksa'].strftime('%d/%m/%Y'), 'detail': i['HasilKomponenPeriksa']} for i in komponen]
    return result
