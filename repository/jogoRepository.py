from typing import Any

from db import acessando_base
from models.jogo import *
from utils import converteDictEmJsonAll

import json

def findAllJogo() -> list[dict[Any, Any]]:
    con = acessando_base()  # faz a conexao com o banco
    # query = "SELECT * FROM jogo;"  # faz monta q query
    query = '''
        SELECT
          JSON_PRETTY(
              JSON_ARRAYAGG(JSON_OBJECT('id', j.id, 'nome', j.nome, 'usuarios', s.usuarios, 'categorias', cs.categorias, 'consoles', csn.consoles))) AS jogos
            FROM
                connect_store.jogo j
            left join (
                SELECT u.id, 
                    JSON_ARRAYAGG(JSON_OBJECT('id', u.id, 'name', u.nome, 'username', u.username, 'email', u.email)) AS usuarios  
                FROM 
                    connect_store.usuario u 
            GROUP BY u.id) s ON s.id = j.usuario_id
            left join (
                SELECT c.id, 
                    JSON_ARRAYAGG(JSON_OBJECT('id', c.id, 'nome', c.nome)) AS categorias  
                FROM 
                    connect_store.categoria c 
            GROUP BY c.id) cs ON cs.id = j.categoria_id
            left join (
                SELECT con.id, 
                    JSON_ARRAYAGG(JSON_OBJECT('id', con.id, 'nome', con.nome)) AS consoles
                FROM 
                    connect_store.console con 
            GROUP BY con.id) csn ON csn.id = j.console_id;
    '''
    cursor = con.cursor()
    cursor.execute(query)

    result = converteDictEmJsonAll(cursor)  # faz a busca no banco e formata o retorno

    if con.is_connected():
        con.close()
        cursor.close()

    if result[0]['jogos'] != None:
        return json.loads(result[0]['jogos'])  # retorna somente o objeto JSON
    else:
        return None

def findByIdJogo(id: int) -> Jogo|None:

    con = acessando_base() # faz a conexao com o banco
    # query = "SELECT * FROM jogo WHERE id = {}".format(id)  # faz monta q query
    query = '''
            SELECT
              JSON_PRETTY(
                  JSON_ARRAYAGG(JSON_OBJECT('id', j.id, 'nome', j.nome, 'usuarios', s.usuarios, 'categorias', cs.categorias, 'consoles', csn.consoles))) AS jogos
                FROM
                    connect_store.jogo j
                left join (
                    SELECT u.id, 
                        JSON_ARRAYAGG(JSON_OBJECT('id', u.id, 'name', u.nome, 'username', u.username, 'email', u.email)) AS usuarios  
                    FROM 
                        connect_store.usuario u 
                GROUP BY u.id) s ON s.id = j.usuario_id
                left join (
                    SELECT c.id, 
                        JSON_ARRAYAGG(JSON_OBJECT('id', c.id, 'nome', c.nome)) AS categorias  
                    FROM 
                        connect_store.categoria c 
                GROUP BY c.id) cs ON cs.id = j.categoria_id
                left join (
                    SELECT con.id, 
                        JSON_ARRAYAGG(JSON_OBJECT('id', con.id, 'nome', con.nome)) AS consoles
                    FROM 
                        connect_store.console con 
                GROUP BY con.id) csn ON csn.id = j.console_id
                WHERE j.id = {};
    '''.format(id)
    cursor = con.cursor()
    cursor.execute(query) # faz a busca no banco

    result = converteDictEmJsonAll(cursor) # faz a busca no banco e formata o retorno e retorna somente 1 dado

    if con.is_connected():
        con.close()
        cursor.close()

    if result[0]['jogos'] != None:
        return json.loads(result[0]['jogos'])[0]  # retorna somente o objeto JSON
    else:
        return None

def findByNomeJogo(nome: str) -> Jogo|None:

    con = acessando_base() # faz a conexao com o banco
    query = "SELECT * FROM jogo WHERE nome = '{}'".format(nome)  # faz monta q query
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

def postJogo(jogo: Jogo) -> str:

    if findByNomeJogo(jogo['nome']) == None:
        con = acessando_base() # faz a conexao com o banco
        query = "INSERT INTO jogo (nome, img, categoria_id, console_id, usuario_id) VALUES ('{}', '{}', {}, {}, {});".format(jogo['nome'], jogo['img'], jogo['categoria_id'], jogo['console_id'], jogo['usuario_id'])  # faz monta q query
        cursor = con.cursor()
        result = cursor.execute(query) # faz a busca no banco
        con.commit() # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        return 'Jogo cadastrado com sucesso!'

    return 'Jogo ja existe na base.'

def putJogo(jogo: Jogo) -> str:

    if findByIdJogo(jogo['id']) != None:
        con = acessando_base() # faz a conexao com o banco
        query = "UPDATE jogo SET nome = '{}', img = '{}', categoria_id = {} , console_id = {}, usuario_id = {} WHERE id = {};".format(jogo['nome'], jogo['img'], jogo['categoria_id'], jogo['console_id'], jogo['usuario_id'], jogo['id'])  # faz monta q query
        cursor = con.cursor()
        cursor.execute(query) # faz a busca no banco
        con.commit() # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        return 'Jogo atualizado com sucesso!'

    return 'Nao foi localizado esse jogo cadastrado na base.'

def deleteByIdJogo(id: int) -> str:

    if findByIdJogo(id) != None:
        con = acessando_base() # faz a conexao com o banco
        query = "DELETE FROM jogo WHERE id = {};".format(id)  # faz monta q query

        cursor = con.cursor()
        cursor.execute(query) # faz a busca no banco
        con.commit()  # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        return 'Jogo deletado com sucesso!'

    return 'Nao foi possivel excluir o jogo da base, pois ele nao foi localizado.'