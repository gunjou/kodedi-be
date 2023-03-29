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
        text(f"""SELECT * FROM Pasien_M;""")
    )
    return result

# def get_no_verif():
#     result = engine.execute(
#         text(f"""SELECT NoVerifikasi FROM Pasien_M WHERE = '230320%';""")
#     )
#     return result

def get_no_cm():
    result = engine.execute(
        text(f"""SELECT NoCM FROM Pasien_M;""")
    )
    return result

def query_add_pasien(KdProfile, NoCM, KdTitle, NamaLengkap, NamaKeluarga, NamaPanggilan, NamaDepan, NamaTengah, NamaBelakang, KdJenisKelamin, TglLahir, KdNegara, StatusEnabled, NoVerifikasi, NoRec):
    engine.execute(
        text(f"""INSERT INTO Pasien_M  (KdProfile, NoCM, KdTitle, NamaLengkap, NamaKeluarga, NamaPanggilan, NamaDepan, NamaTengah, NamaBelakang, KdJenisKelamin, TglLahir, KdNegara, StatusEnabled, NoVerifikasi, NoRec)
                VALUES ({KdProfile}, '{NoCM}', {KdTitle}, '{NamaLengkap}', '{NamaKeluarga}', '{NamaPanggilan}', '{NamaDepan}', '{NamaTengah}', '{NamaBelakang}', {KdJenisKelamin}, '{TglLahir}', {KdNegara}, {StatusEnabled}, {NoVerifikasi}, '{NoRec}');""")
    )