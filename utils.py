import json, base64, time

from db import acessando_base
from models.usuario import Usuario
from connectStore import app


def converteDictEmJsonAll(cursor):
    lista = cursor.fetchall()

    if lista:
        return [dict(dict_factory(cursor, row)) for row in lista]
    else:
        return []


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def validaToken(token) -> bool:
    data = base64.b64decode(token).decode("utf-8")

    username = data.split(':')[0]
    senha = data.split(':')[1]

    usuario = findByUsuarioBanco(username, senha)

    if usuario:
        if usuario['senha'].__eq__(senha):
            return True

    return False


def findByUsuarioBanco(username: str, senha: str) -> Usuario | None:
    con = acessando_base()  # faz a conexao com o banco
    query = "SELECT * FROM usuario WHERE username = '{}' and senha = '{}'".format(username, senha)  # faz monta q query
    cursor = con.cursor()
    cursor.execute(query)  # faz a busca no banco

    result = converteDictEmJsonAll(cursor)  # faz a busca no banco e formata o retorno e retorna somente 1 dado

    if con.is_connected():
        con.close()
        cursor.close()

    if result[0] != None:
        return result[0]  # retorna somente o objeto JSON
    else:
        return None


def uploadImagemRepositorio(file, pasta: str):
    try:
        # GERAR OBJ IMAGEM
        arquivo = file

        uploads_path = app.config['UPLOAD_PATH'] + f'\\{pasta}'

        timeStamp = str(time.time()).replace('.', '-')

        nomeArquivo = f'capa-{timeStamp}.jpg'

        arquivo.save(f'{uploads_path}\\{nomeArquivo}')

        return nomeArquivo
    except:
        return None
