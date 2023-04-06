from datetime import date
import uuid
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import text


from api.query import get_list_patient, query_add_pasien, get_no_cm

from api.config import get_connection


engine = get_connection()

master_bp = Blueprint('api', __name__)

@master_bp.route('/api/master/data-title', methods=['GET'])
def data_title():
    data = engine.execute(text(f"""SELECT KdTitle, NamaTitle FROM Title_M;"""))
    result = [{'id': row['KdTitle'], 'nama': row['NamaTitle']} for row in data]
    return result

@master_bp.route('/api/master/data-jeniskelamin', methods=['GET'])
def data_jeniskelamin():
    data = engine.execute(text(f"""SELECT KdJenisKelamin, JenisKelamin FROM JenisKelamin_M;"""))
    result = [{'id': row['KdJenisKelamin'], 'jk': row['JenisKelamin']} for row in data]
    return result

@master_bp.route('/api/master/data-negara', methods=['GET'])
def data_negara():
    data = engine.execute(text(f"""SELECT KdNegara, NamaNegara FROM Negara_M;"""))
    result = [{'id': row['KdNegara'], 'negara': row['NamaNegara']} for row in data]
    return result

@master_bp.route('/api/master/komponen-anamnesis', methods=['GET'])
def komponen_anamnesis():
    data = engine.execute(text(f"""SELECT KdKomponen, NamaKomponen, KdKomponenHead, NoUrut FROM Komponen_M WHERE StatusEnabled = 1 AND KdKomponenHead = 1;"""))
    result = [{'id': row['KdKomponen'], 'no': row['NoUrut'], 'komponen': row['NamaKomponen'], 'kode_head': row['KdKomponenHead']} for row in data]
    return result

@master_bp.route('/api/master/hasil-anamnesis', methods=['GET'])
def hasil_anamnesis():
    data = engine.execute(text(f"""SELECT KdKomponenHasil, NamaKomponenHasil, KdKomponenHasilHead, NoUrut FROM KomponenHasil_M WHERE KdKomponenHasilHead = 1;"""))
    result = [{'id': row['KdKomponenHasil'], 'no': row['NoUrut'], 'hasil': row['NamaKomponenHasil'], 'kode_head': row['KdKomponenHasilHead']} for row in data]
    return result

@master_bp.route('/api/master/tanda-vital', methods=['GET'])
def master_tanda_vital():
    data = engine.execute(
        text(f"""SELECT k.KdKomponen, k.NamaKomponen, k.KdKomponenHead, k.NoUrut, s.KdSatuanHasil, s.SatuanHasil
                FROM Komponen_M k FULL OUTER JOIN SatuanHasil_M s ON k.KdSatuanHasil = s.KdSatuanHasil
                WHERE k.StatusEnabled = 1 AND k.KdKomponenHead = 2;"""))
    result = [{'id': row['KdKomponen'], 'no': row['NoUrut'], 'komponen': row['NamaKomponen'], 'kode_head': row['KdKomponenHead'], 'kode_satuan': row['KdSatuanHasil'], 'satuan': row['SatuanHasil']} for row in data]
    return result