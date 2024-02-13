from typing import List, Dict, Any

from db import acessando_base
from models.usuario import *

def converteDictEmJsonAll(cursor):
    lista = cursor.fetchall()

    if lista:
        return [dict(dict_factory(cursor, row)) for row in lista]
    else:
        return []

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def findAllUsuarios() -> list[dict[Any, Any]]:
    con = acessando_base() # faz a conexao com o banco
    query = "SELECT * FROM usuario;" # faz monta q query
    cursor = con.cursor()
    cursor.execute(query)

    result = converteDictEmJsonAll(cursor) # faz a busca no banco e formata o retorno

    if con.is_connected():
        con.close()
        cursor.close()

    return result

def findByIdUsuario(id: int) -> Usuario|None:
    con = acessando_base() # faz a conexao com o banco
    query = "SELECT * FROM usuario WHERE id = {}".format(id)  # faz monta q query
    cursor = con.cursor()
    cursor.execute(query) # faz a busca no banco

    result = converteDictEmJsonAll(cursor) # faz a busca no banco e formata o retorno e retorna somente 1 dado

    if con.is_connected():
        con.close()
        cursor.close()

    if result:
        return result[0]
    else:
        return None

def findByUsernameUsuario(username: str) -> Usuario|None:

    con = acessando_base() # faz a conexao com o banco
    query = "SELECT * FROM usuario WHERE username = '{}'".format(username)  # faz monta q query
    cursor = con.cursor()
    cursor.execute(query) # faz a busca no banco

    result = converteDictEmJsonAll(cursor) # faz a busca no banco e formata o retorno e retorna somente 1 dado

    if con.is_connected():
        con.close()
        cursor.close()

    if result:
        return result[0]
    else:
        return None

def postUsuario(usuario: Usuario) -> str:

    if findByUsernameUsuario(usuario['username']) == None:
        con = acessando_base() # faz a conexao com o banco
        query = "INSERT INTO usuario (nome, username, email, senha) VALUES ('{}', '{}', '{}', '{}');".format(usuario['nome'], usuario['username'], usuario['email'], usuario['senha'])  # faz monta q query
        cursor = con.cursor()
        result = cursor.execute(query) # faz a busca no banco
        con.commit() # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        return 'Usuario cadastrado com sucesso!'

    return 'Usuario ja existe na base.'

def putUsuario(usuario: Usuario) -> str:

    if findByIdUsuario(usuario['id']) != None:
        con = acessando_base() # faz a conexao com o banco
        query = "UPDATE usuario SET nome = '{}', username = '{}', email = '{}', senha = '{}' WHERE id = {};".format(usuario['nome'], usuario['username'], usuario['email'], usuario['senha'], usuario['id'])  # faz monta q query
        cursor = con.cursor()
        result = cursor.execute(query) # faz a busca no banco
        con.commit() # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        return 'Usuario atualizado com sucesso!'

    return 'Nao foi localizado esse usuario cadastrado na base'

def deleteByIdUsuario(id: int) -> str:

    if findByIdUsuario(id) != None:
        con = acessando_base() # faz a conexao com o banco
        query = "DELETE FROM usuario WHERE id = {};".format(id)  # faz monta q query

        cursor = con.cursor()
        cursor.execute(query) # faz a busca no banco
        con.commit()  # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        return 'Usuario deletado com sucesso!'

    return 'Nao foi possivel excluir o usuario da base, pois ele nao foi localizado.'

def loginUsuario(usuario: Usuario):

    if usuario['username'] != '' and usuario['senha'] != '':

        con = acessando_base()  # faz a conexao com o banco
        query = "SELECT * FROM usuario WHERE username = '{}' and senha = '{}'".format(usuario['username'], usuario['senha'])  # faz monta q query
        cursor = con.cursor()
        cursor.execute(query)  # faz a busca no banco

        result = converteDictEmJsonAll(cursor)  # faz a busca no banco e formata o retorno e retorna somente 1 dado

        if con.is_connected():
            con.close()
            cursor.close()

        if result:
            return result[0]
        else:
            return None

    return None