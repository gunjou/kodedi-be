from datetime import date
import uuid
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import text


from api.query import get_list_patient, query_add_pasien, get_no_cm

from api.config import get_connection


engine = get_connection()

master_bp = Blueprint('api', __name__)

@master_bp.route('/master/data-title', methods=['GET'])
def data_title():
    data = engine.execute(text(f"""SELECT KdTitle, NamaTitle FROM Title_M;"""))
    result = [{'id': row['KdTitle'], 'nama': row['NamaTitle']} for row in data]
    return result

@master_bp.route('/master/data-jeniskelamin', methods=['GET'])
def data_jeniskelamin():
    data = engine.execute(text(f"""SELECT KdJenisKelamin, JenisKelamin FROM JenisKelamin_M;"""))
    result = [{'id': row['KdJenisKelamin'], 'jk': row['JenisKelamin']} for row in data]
    return result

@master_bp.route('/master/data-negara', methods=['GET'])
def data_negara():
    data = engine.execute(text(f"""SELECT KdNegara, NamaNegara FROM Negara_M;"""))
    result = [{'id': row['KdNegara'], 'negara': row['NamaNegara']} for row in data]
    return result