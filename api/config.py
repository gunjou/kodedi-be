from urllib.parse import quote_plus
from sqlalchemy import create_engine


def get_connection():
    server = 'bottis.id'
    database = 'Kodedi'
    username = 'sa'
    password = r'@DBJ4s4medik4@'
    return create_engine(f'mssql+pymssql://{username}:%s@{server}:20000/{database}' % quote_plus(password))
