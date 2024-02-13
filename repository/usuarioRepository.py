from typing import List, Dict, Any

from db import acessando_base
from models.usuario import *
from utils import converteDictEmJsonAll

import json

def findAllUsuarios() -> list[dict[Any, Any]]:
    con = acessando_base() # faz a conexao com o banco
    # query = "SELECT * FROM usuario;" # faz monta q query
    query = '''
        SELECT
          JSON_PRETTY(
              JSON_ARRAYAGG(JSON_OBJECT('id', u.id, 'name', u.nome, 'username', u.username, 'email', u.email, 'consoles', s.consoles))) AS usuarios 
            FROM
                connect_store.usuario u
            left join (
                SELECT usuario_id, 
                    JSON_ARRAYAGG(JSON_OBJECT('id', c.id, 'nome', c.nome)) AS consoles 
                FROM 
                    connect_store.console c 
            GROUP BY c.usuario_id) s ON s.usuario_id = u.id;
    '''
    cursor = con.cursor()
    cursor.execute(query)

    result = converteDictEmJsonAll(cursor) # faz a busca no banco e formata o retorno

    if con.is_connected():
        con.close()
        cursor.close()

    if result[0]['usuarios'] != None:
        return json.loads(result[0]['usuarios']) # retorna somente o objeto JSON
    else:
        return None

def findByIdUsuario(id: int) -> Usuario|None:
    con = acessando_base() # faz a conexao com o banco
    # query = "SELECT * FROM usuario WHERE id = {}".format(id)  # faz monta q query
    query = '''SELECT
                  JSON_PRETTY(
                      JSON_ARRAYAGG(JSON_OBJECT('id', u.id, 'name', u.nome, 'username', u.username, 'email', u.email, 'consoles', s.consoles))) AS usuarios 
                    FROM
                        connect_store.usuario u
                    left join (
                        SELECT usuario_id, 
                            JSON_ARRAYAGG(JSON_OBJECT('id', c.id, 'nome', c.nome)) AS consoles 
                        FROM 
                            connect_store.console c 
                    GROUP BY c.usuario_id) s ON s.usuario_id = u.id 
                    WHERE u.id = {};
    '''.format(id)
    cursor = con.cursor()
    cursor.execute(query) # faz a busca no banco

    result = converteDictEmJsonAll(cursor) # faz a busca no banco e formata o retorno e retorna somente 1 dado

    if con.is_connected():
        con.close()
        cursor.close()

    if result[0]['usuarios'] != None:
        return json.loads(result[0]['usuarios'])[0]  # retorna somente o objeto JSON
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