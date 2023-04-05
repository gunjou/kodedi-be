from urllib.parse import quote_plus
from sqlalchemy import create_engine


def get_connection():
    # server = '192.168.1.249'
    # port = 1433
    server = 'bottis.id'
    port = 20000
    database = 'Kodedi'
    username = 'sa'
    password = r'@DBJ4s4medik4@'
    return create_engine(f'mssql+pymssql://{username}:%s@{server}:{port}/{database}' % quote_plus(password))
