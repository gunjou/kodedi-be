from sqlalchemy import text

from api.config import get_connection


engine = get_connection()

def get_id():
    result = engine.execute(text(f"""SELECT MAX(KdUser) FROM LoginUser_S;"""))
    return result

def check_user(username):
    result = engine.execute(text(f"""SELECT * from LoginUser_s WHERE NamaUserMobile = '{username}';"""))
    return result

def create_user(KdUser, NamaUserMobile, NamaLengkap, NamaUserEmail, KataSandi, TglDaftar, KdProfile, StatusEnabled, NoRec):
    engine.execute(
        text(f"""INSERT INTO LoginUser_S  (KdUser, NamaUserMobile, NamaLengkap, NamaUserEmail, KataSandi, TglDaftar, KdProfile, StatusEnabled, NoRec)
                VALUES ({KdUser}, '{NamaUserMobile}', '{NamaLengkap}', '{NamaUserEmail}', '{KataSandi}', '{TglDaftar}', {KdProfile}, {StatusEnabled}, '{NoRec}');""")
    )

def get_data_user(no_rec):
    result = engine.execute(
        text(f"""SELECT * FROM LoginUser_S WHERE NoRec = '{no_rec}';""")
    )
    return result

def get_list_patient():
    result = engine.execute(
        # text(f"""SELECT * FROM Pasien_M;""")
        text(f"""SELECT pm.*, svt.KodeVerifikasi FROM Pasien_M pm JOIN StrukVerifikasi_T svt ON pm.NoVerifikasi = svt.NoVerifikasi WHERE pm.StatusEnabled = 1 AND svt.StatusEnabled = 1;""")
    )
    return result

def get_detail_patient(no_cm):
    result = engine.execute(
        text(f"""SELECT * FROM Pasien_M WHERE NoCM = {no_cm};""")
    )
    return result

def get_no_verif(no):
    result = engine.execute(
        text(f"""SELECT NoVerifikasi FROM StrukVerifikasi_T WHERE NoVerifikasi LIKE '{no}%';""")
    )
    return result

def get_no_cm():
    result = engine.execute(
        text(f"""SELECT NoCM FROM Pasien_M;""")
    )
    return result

def query_add_verifikasi(KdProfile, NoVerifikasi, TglVerifikasi, KodeVerifikasi, StatusEnabled, NoRec):
    engine.execute(
        text(f"""INSERT INTO StrukVerifikasi_T (KdProfile, NoVerifikasi, TglVerifikasi, KodeVerifikasi, StatusEnabled, NoRec)
                VALUES ({KdProfile}, '{NoVerifikasi}', '{TglVerifikasi}', {KodeVerifikasi}, {StatusEnabled}, '{NoRec}');""")
    )

def query_add_pasien(KdProfile, NoCM, KdTitle, NamaLengkap, KdJenisKelamin, TglLahir, KdNegara, StatusEnabled, NoVerifikasi, NoRec):
    engine.execute(
        text(f"""INSERT INTO Pasien_M  (KdProfile, NoCM, KdTitle, NamaLengkap, KdJenisKelamin, TglLahir, KdNegara, StatusEnabled, NoVerifikasi, NoRec)
                VALUES ({KdProfile}, '{NoCM}', {KdTitle}, '{NamaLengkap}', {KdJenisKelamin}, '{TglLahir}', {KdNegara}, {StatusEnabled}, {NoVerifikasi}, '{NoRec}');""")
    )

def query_delete_patient(NoCM):
    engine.execute(text(f"UPDATE Pasien_M  SET StatusEnabled = 0 WHERE NoCM = '{NoCM}';"))

def get_no_periksa():
    result = engine.execute(text(f'SELECT NoHasilPeriksa FROM HasilPemeriksaan_T;'))
    return result

def get_master_komponen_anamnesis(KdKomponen):
    result = engine.execute(
        text(f"""SELECT NamaKomponenHasil FROM KomponenHasil_M WHERE KdKomponenHasil = {KdKomponen};""")
    )
    return result

def query_add_hasil_periksa(KdProfile, NoHasilPeriksa, NoCM, TglHasilPeriksa, StatusEnabled, NoRec, no_verif):
    engine.execute(
        text(f"""INSERT INTO HasilPemeriksaan_T  (KdProfile, NoHasilPeriksa, NoCM, TglHasilPeriksa, StatusEnabled, NoRec)
                VALUES ({KdProfile}, {NoHasilPeriksa}, '{NoCM}', '{TglHasilPeriksa}', {StatusEnabled}, '{NoRec}');""")
    )
    engine.execute(text(f"UPDATE Pasien_M SET NoVerifikasi = {no_verif} WHERE NoCM = {NoCM}"))
    

def query_add_detail_hasil_periksa(KdProfile, NoHasilPeriksa, TglHasilPeriksa, StatusEnabled, NoRec, KdKomponenPeriksa, HasilKomponenPeriksa):
    engine.execute(
        text(f"""INSERT INTO HasilPemeriksaanD_T  (KdProfile, NoHasilPeriksa, KdKomponenPeriksa, TglHasilKomponenPeriksa, HasilKomponenPeriksa, StatusEnabled, NoRec)
                VALUES ({KdProfile}, {NoHasilPeriksa}, {KdKomponenPeriksa}, '{TglHasilPeriksa}', '{HasilKomponenPeriksa}', {StatusEnabled}, '{NoRec}');""")
    )

def get_anamnesis(no_cm):
    result = engine.execute(
        text(f"""SELECT NamaKomponen, hp.TglHasilKomponenPeriksa, hp.HasilKomponenPeriksa
                FROM HasilPemeriksaanD_T hp
                JOIN Komponen_M km 
                ON hp.KdKomponenPeriksa = km.KdKomponen
                JOIN HasilPemeriksaan_T hpt 
                ON hpt.NoHasilPeriksa = hp.NoHasilPeriksa
                WHERE hpt.NoCM = {no_cm} AND km.KdKomponen < 31""")
    )
    return result

def get_master_anamnesis():
    result = engine.execute(text("SELECT KdKomponen, NamaKomponen, ReportDisplay FROM Komponen_M WHERE StatusEnabled = 1 AND KdKomponenHead = 1;"))
    return result

def get_tanda_vital(no_cm):
    result = engine.execute(
        text(f"""SELECT NamaKomponen, hp.TglHasilKomponenPeriksa, hp.HasilKomponenPeriksa
                FROM HasilPemeriksaanD_T hp
                JOIN Komponen_M km 
                ON hp.KdKomponenPeriksa = km.KdKomponen
                JOIN HasilPemeriksaan_T hpt 
                ON hpt.NoHasilPeriksa = hp.NoHasilPeriksa
                WHERE hpt.NoCM = {no_cm} AND km.KdKomponen > 30 AND km.KdKomponen < 38;""")
    )
    return result
