from sqlalchemy import text

from api.config import get_connection


engine = get_connection()

def get_id():
    result = engine.execute(text(f"""SELECT MAX(KdUser) FROM LoginUser_S;"""))
    return result

def check_user(username):
    result = engine.execute(text(f"""SELECT * from LoginUser_s WHERE NamaUserMobile = {username};"""))
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