import os

SECRET_KEY = 'connectStore'

URI = '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGBD='mysql+mysqlconnector',
    usuario='kneri',
    senha='123456',
    servidor='localhost',
    database='connect_store'
)

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\uploads'