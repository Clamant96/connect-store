from typing import Any

from db import acessando_base
from models.console import *
from utils import converteDictEmJsonAll

import json

def findAllConsole() -> list[dict[Any, Any]]:
    con = acessando_base()  # faz a conexao com o banco
    # query = "SELECT * FROM console;"  # faz monta q query
    query = '''
        SELECT
          JSON_PRETTY(
              JSON_ARRAYAGG(JSON_OBJECT('id', c.id, 'nome', c.nome, 'icone', c.icone, 'usuarios', s.usuarios))) AS consoles
            FROM
                connect_store.console c
            left join (
                SELECT u.id, 
                    JSON_OBJECT('id', u.id, 'name', u.nome, 'username', u.username, 'email', u.email) AS usuarios  
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

    if result[0]['consoles'] != None:
        return json.loads(result[0]['consoles'])  # retorna somente o objeto JSON
    else:
        return None

def findByIdConsole(id: int) -> Console|None:

    con = acessando_base() # faz a conexao com o banco
    # query = "SELECT * FROM console WHERE id = {}".format(id)  # faz monta q query
    query = '''
        SELECT
          JSON_PRETTY(
              JSON_ARRAYAGG(JSON_OBJECT('id', c.id, 'nome', c.nome, 'icone', c.icone, 'usuarios', s.usuarios))) AS consoles
            FROM
                connect_store.console c
            left join (
                SELECT u.id, 
                    JSON_OBJECT('id', u.id, 'name', u.nome, 'username', u.username, 'email', u.email) AS usuarios  
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

    if result[0]['consoles'] != None:
        return json.loads(result[0]['consoles'])[0]  # retorna somente o objeto JSON
    else:
        return None

def findByNomeConsole(nome: str) -> Console|None:

    con = acessando_base() # faz a conexao com o banco
    query = "SELECT * FROM console WHERE nome = '{}'".format(nome)  # faz monta q query
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

def postConsole(console: Console):

    if findByNomeConsole(console['nome']) == None:
        con = acessando_base() # faz a conexao com o banco
        query = "INSERT INTO console (nome, icone, usuario_id) VALUES ('{}', '{}', {});".format(console['nome'], console['icone'], console['usuario_id'])  # faz monta q query
        cursor = con.cursor()
        result = cursor.execute(query) # faz a busca no banco
        con.commit() # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        return findByNomeConsole(console['nome'])

    return 'Console ja existe na base.'

def putConsole(console: Console):

    print(findByIdConsole(console['id']))

    if findByIdConsole(console['id']) != None:
        con = acessando_base() # faz a conexao com o banco
        query = "UPDATE console SET nome = '{}', icone = '{}', usuario_id = {} WHERE id = {};".format(console['nome'], console['icone'], console['usuario_id'], console['id'])  # faz monta q query
        cursor = con.cursor()
        cursor.execute(query) # faz a busca no banco
        con.commit() # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        return findByIdConsole(console['id'])

    return 'Nao foi localizado esse console cadastrado na base.'

def deleteByIdConsole(id: int) -> str:

    if findByIdConsole(id) != None:

        # DEVIDO AOS RELACIONAMENTOS DAS TANELAS, TEMOS QUE DELETAR ELES ANTES DE DELETAR O OBJETO PRINCIPAL
        if deleteConsolesByIdCategoria(id) != '':
            print(f'Consoles excluidos com sucesso da tabela auxiliar.')

        con = acessando_base() # faz a conexao com o banco
        query = "DELETE FROM console WHERE id = {};".format(id)  # faz monta q query

        cursor = con.cursor()
        cursor.execute(query) # faz a busca no banco
        con.commit()  # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        return 'Console deletado com sucesso!'

    return 'Nao foi possivel excluir o console da base, pois ele nao foi localizado.'

def deleteConsolesByIdCategoria(id: int) -> str:
    con = acessando_base()  # faz a conexao com o banco
    query = "DELETE FROM connect_store.categoria_console AS cj WHERE cj.console_id = {};".format(id)  # faz monta q query

    cursor = con.cursor()
    cursor.execute(query)  # faz a busca no banco
    con.commit()  # registrar os dados no banco

    if con.is_connected():
        con.close()
        cursor.close()

    return 'Consoles removidos da categoria com sucesso!'