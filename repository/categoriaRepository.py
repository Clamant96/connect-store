from typing import Any

from db import acessando_base
from models.categoria import *
from utils import converteDictEmJsonAll

import json

def findAllCategoria() -> list[dict[Any, Any]]:
    con = acessando_base()  # faz a conexao com o banco
    # query = "SELECT * FROM categoria;"  # faz monta q query
    query = '''
        SELECT
          JSON_PRETTY(
              JSON_ARRAYAGG(JSON_OBJECT('id', c.id, 'nome', c.nome, 'usuarios', s.usuarios))) AS categorias
            FROM
                connect_store.categoria c
            left join (
                SELECT u.id, 
                    JSON_ARRAYAGG(JSON_OBJECT('id', u.id, 'name', u.nome, 'username', u.username, 'email', u.email)) AS usuarios  
                FROM 
                    connect_store.usuario u 
            GROUP BY u.id) s ON s.id = c.usuario_id;
    '''
    cursor = con.cursor()
    cursor.execute(query)

    result = converteDictEmJsonAll(cursor)  # faz a busca no banco e formata o retorno

    if con.is_connected():
        con.close()
        cursor.close()

    print(result)

    if result[0]['categorias'] != None:
        return json.loads(result[0]['categorias'])  # retorna somente o objeto JSON
    else:
        return None

def findByIdCategoria(id: int) -> Categoria|None:

    con = acessando_base() # faz a conexao com o banco
    # query = "SELECT * FROM categoria WHERE id = {}".format(id)  # faz monta q query
    query = '''
        SELECT
          JSON_PRETTY(
              JSON_ARRAYAGG(JSON_OBJECT('id', c.id, 'nome', c.nome, 'usuarios', s.usuarios))) AS categorias
            FROM
                connect_store.categoria c
            left join (
                SELECT u.id, 
                    JSON_ARRAYAGG(JSON_OBJECT('id', u.id, 'name', u.nome, 'username', u.username, 'email', u.email)) AS usuarios  
                FROM 
                    connect_store.usuario u 
            GROUP BY u.id) s ON s.id = c.usuario_id
            WHERE c.id = {};
    '''.format(id)
    cursor = con.cursor()
    cursor.execute(query) # faz a busca no banco

    result = converteDictEmJsonAll(cursor) # faz a busca no banco e formata o retorno e retorna somente 1 dado

    if con.is_connected():
        con.close()
        cursor.close()

    if result[0]['categorias'] != None:
        return json.loads(result[0]['categorias'])[0]  # retorna somente o objeto JSON
    else:
        return None

def findByNomeCategoria(nome: str) -> Categoria|None:

    con = acessando_base() # faz a conexao com o banco
    query = "SELECT * FROM categoria WHERE nome = '{}'".format(nome)  # faz monta q query
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

def postCategoria(categoria: Categoria) -> str:

    if findByNomeCategoria(categoria['nome']) == None:
        con = acessando_base() # faz a conexao com o banco
        query = "INSERT INTO categoria (nome, usuario_id) VALUES ('{}', {});".format(categoria['nome'], categoria['usuario_id'])  # faz monta q query
        cursor = con.cursor()
        result = cursor.execute(query) # faz a busca no banco
        con.commit() # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        return 'Categoria cadastrado com sucesso!'

    return 'Categoria ja existe na base.'

def putCategoria(categoria: Categoria) -> str:

    if findByIdCategoria(categoria['id']) != None:
        con = acessando_base() # faz a conexao com o banco
        query = "UPDATE categoria SET nome = '{}', usuario_id = {} WHERE id = {};".format(categoria['nome'], categoria['usuario_id'], categoria['id'])  # faz monta q query
        cursor = con.cursor()
        cursor.execute(query) # faz a busca no banco
        con.commit() # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        return 'Console atualizado com sucesso!'

    return 'Nao foi localizado essa categoria cadastrado na base.'

def deleteByIdCategoria(id: int) -> str:

    if findByIdCategoria(id) != None:
        con = acessando_base() # faz a conexao com o banco
        query = "DELETE FROM categoria WHERE id = {};".format(id)  # faz monta q query

        cursor = con.cursor()
        cursor.execute(query) # faz a busca no banco
        con.commit()  # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        return 'Categoria deletada com sucesso!'

    return 'Nao foi possivel excluir a categoria da base, pois ele nao foi localizado.'