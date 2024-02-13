SECRET_KEY = 'connectStore'

URI = '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGBD='mysql+mysqlconnector',
    usuario='kneri',
    senha='123456',
    servidor='localhost',
    database='connect_store'
)