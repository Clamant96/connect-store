from typing import Any

from db import acessando_base
from models.categoria import *
from utils import converteDictEmJsonAll
from connectStore import findByIdConsole

import json

def findAllCategoria() -> list[dict[Any, Any]]:
    con = acessando_base()  # faz a conexao com o banco
    # query = "SELECT * FROM categoria;"  # faz monta q query
    query = '''
        SELECT
          JSON_PRETTY(
              JSON_ARRAYAGG(JSON_OBJECT('id', c.id, 'nome', c.nome, 'uri', c.uri, 'img', c.img, 'usuarios', s.usuarios))) AS categorias
            FROM
                connect_store.categoria c
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
              JSON_ARRAYAGG(JSON_OBJECT('id', c.id, 'nome', c.nome, 'uri', c.uri, 'img', c.img, 'usuarios', s.usuarios))) AS categorias
            FROM
                connect_store.categoria c
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

def findAllJogosComSeusConsolesEUsuarioCategoria() -> Categoria|None:

    con = acessando_base() # faz a conexao com o banco
    # query = "SELECT * FROM categoria WHERE id = {}".format(id)  # faz monta q query
    query = '''
        SELECT 
                JSON_PRETTY(
                  JSON_ARRAYAGG(JSON_OBJECT('id', c.id, 'nome', c.nome, 'uri', c.uri, 'img', c.img, 'jogos', cs.jogos, 'usuarios', s.usuarios, 'consoles', csn.consoles))) AS categorias
            FROM 
                connect_store.categoria AS c 
                
                    left join (
                        SELECT j.categoria_id, 
                            JSON_ARRAYAGG(JSON_OBJECT('id', j.id, 'nome', j.nome, 'img', j.img, 'preco', j.preco, 'desconto', j.desconto, 'consoles', csn.consoles)) AS jogos
                        FROM 
                            connect_store.jogo AS j 
                            
                                left join (
                                    SELECT cc.jogo_id, 
                                        JSON_ARRAYAGG(JSON_OBJECT('id', con.id, 'nome', con.nome, 'icone', con.icone)) AS consoles
                                    FROM 
                                        connect_store.console AS con 
                                            left join 
                                                connect_store.jogo_console AS cc 
                                            ON con.id = cc.console_id 
                                    GROUP BY cc.jogo_id) csn 
                                ON j.id = csn.jogo_id
                            
                        GROUP BY j.categoria_id) cs ON cs.categoria_id = c.id
                    left join (
                        SELECT u.id, 
                            JSON_OBJECT('id', u.id, 'name', u.nome, 'username', u.username, 'email', u.email) AS usuarios  
                        FROM 
                            connect_store.usuario u 
                    GROUP BY u.id) s ON s.id = c.usuario_id
                left join (
                    SELECT cc.categoria_id, 
                        JSON_ARRAYAGG(JSON_OBJECT('id', con.id, 'nome', con.nome, 'icone', con.icone)) AS consoles
                    FROM 
                        connect_store.categoria AS cat RIGHT JOIN connect_store.categoria_console AS cc ON cc.categoria_id = cat.id LEFT JOIN connect_store.console AS con ON cc.console_id = con.id 
                GROUP BY cc.categoria_id) csn ON csn.categoria_id = c.id;
    '''
    cursor = con.cursor()
    cursor.execute(query) # faz a busca no banco

    result = converteDictEmJsonAll(cursor) # faz a busca no banco e formata o retorno e retorna somente 1 dado

    if con.is_connected():
        con.close()
        cursor.close()

    if result[0]['categorias'] != None:
        return json.loads(result[0]['categorias'])  # retorna somente o objeto JSON
    else:
        return None

def findAllJogosCategoriaById(id: int) -> Categoria|None:

    con = acessando_base() # faz a conexao com o banco
    # query = "SELECT * FROM categoria WHERE id = {}".format(id)  # faz monta q query
    query = '''
        SELECT 
                JSON_PRETTY(
                  JSON_ARRAYAGG(JSON_OBJECT('id', c.id, 'nome', c.nome, 'uri', c.uri, 'img', c.img, 'jogos', cs.jogos, 'usuarios', s.usuarios, 'consoles', csn.consoles))) AS categorias
            FROM 
                connect_store.categoria AS c 
                
                    left join (
                        SELECT j.categoria_id, 
                            JSON_ARRAYAGG(JSON_OBJECT('id', j.id, 'nome', j.nome, 'img', j.img, 'preco', j.preco, 'desconto', j.desconto, 'consoles', csn.consoles)) AS jogos
                        FROM 
                            connect_store.jogo AS j 
                            
                                left join (
                                    SELECT cc.jogo_id, 
                                        JSON_ARRAYAGG(JSON_OBJECT('id', con.id, 'nome', con.nome, 'icone', con.icone)) AS consoles
                                    FROM 
                                        connect_store.console AS con 
                                            left join 
                                                connect_store.jogo_console AS cc 
                                            ON con.id = cc.console_id 
                                    GROUP BY cc.jogo_id) csn 
                                ON j.id = csn.jogo_id
                            
                        GROUP BY j.categoria_id) cs ON cs.categoria_id = c.id
                    left join (
                        SELECT u.id, 
                            JSON_OBJECT('id', u.id, 'name', u.nome, 'username', u.username, 'email', u.email) AS usuarios  
                        FROM 
                            connect_store.usuario u 
                    GROUP BY u.id) s ON s.id = c.usuario_id
                left join (
                    SELECT cc.categoria_id, 
                        JSON_ARRAYAGG(JSON_OBJECT('id', con.id, 'nome', con.nome, 'icone', con.icone)) AS consoles
                    FROM 
                        connect_store.categoria AS cat RIGHT JOIN connect_store.categoria_console AS cc ON cc.categoria_id = cat.id LEFT JOIN connect_store.console AS con ON cc.console_id = con.id 
                GROUP BY cc.categoria_id) csn ON csn.categoria_id = c.id
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

def findAllJogosCategoriaByUri(uri: str) -> Categoria|None:

    con = acessando_base() # faz a conexao com o banco
    # query = "SELECT * FROM categoria WHERE id = {}".format(id)  # faz monta q query
    query = '''
        SELECT 
                JSON_PRETTY(
                  JSON_ARRAYAGG(JSON_OBJECT('id', c.id, 'nome', c.nome, 'uri', c.uri, 'img', c.img, 'jogos', cs.jogos, 'usuarios', s.usuarios, 'consoles', csn.consoles))) AS categorias
            FROM 
                connect_store.categoria AS c 
                
                    left join (
                        SELECT j.categoria_id, 
                            JSON_ARRAYAGG(JSON_OBJECT('id', j.id, 'nome', j.nome, 'img', j.img, 'preco', j.preco, 'desconto', j.desconto, 'consoles', csn.consoles)) AS jogos
                        FROM 
                            connect_store.jogo AS j 
                            
                                left join (
                                    SELECT cc.jogo_id, 
                                        JSON_ARRAYAGG(JSON_OBJECT('id', con.id, 'nome', con.nome, 'icone', con.icone)) AS consoles
                                    FROM 
                                        connect_store.console AS con 
                                            left join 
                                                connect_store.jogo_console AS cc 
                                            ON con.id = cc.console_id 
                                    GROUP BY cc.jogo_id) csn 
                                ON j.id = csn.jogo_id
                            
                        GROUP BY j.categoria_id) cs ON cs.categoria_id = c.id
                    left join (
                        SELECT u.id, 
                            JSON_OBJECT('id', u.id, 'name', u.nome, 'username', u.username, 'email', u.email) AS usuarios  
                        FROM 
                            connect_store.usuario u 
                    GROUP BY u.id) s ON s.id = c.usuario_id
                left join (
                    SELECT cc.categoria_id, 
                        JSON_ARRAYAGG(JSON_OBJECT('id', con.id, 'nome', con.nome, 'icone', con.icone)) AS consoles
                    FROM 
                        connect_store.categoria AS cat RIGHT JOIN connect_store.categoria_console AS cc ON cc.categoria_id = cat.id LEFT JOIN connect_store.console AS con ON cc.console_id = con.id 
                GROUP BY cc.categoria_id) csn ON csn.categoria_id = c.id
            WHERE c.uri = '{}';
    '''.format(uri)
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

def postCategoria(categoria: Categoria) -> str:

    if findByNomeCategoria(categoria['nome']) == None:
        con = acessando_base() # faz a conexao com o banco
        query = "INSERT INTO categoria (nome, uri, img, usuario_id) VALUES ('{}', '{}', '{}', {});".format(categoria['nome'], categoria['uri'], categoria['img'], categoria['usuario_id'])  # faz monta q query
        cursor = con.cursor()
        result = cursor.execute(query) # faz a busca no banco
        con.commit() # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        return 'Categoria cadastrado com sucesso!'

    return 'Categoria ja existe na base.'

def postConsoleEmCategoria(idCategoria: int, idConsole: int) -> str:

    if findByIdCategoria(idCategoria) != None and findByIdConsole(idConsole) != None:
        con = acessando_base() # faz a conexao com o banco
        query = "INSERT INTO connect_store.categoria_console (categoria_id, console_id) VALUES ('{}', {});".format(idCategoria, idConsole)
        cursor = con.cursor()
        result = cursor.execute(query) # faz a busca no banco
        con.commit() # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        return 'Associacao realizada com sucesso!'

    return 'Nao foi possivel associar os dados.'

def putCategoria(categoria: Categoria) -> str:

    if findByIdCategoria(categoria['id']) != None:
        con = acessando_base() # faz a conexao com o banco
        query = "UPDATE categoria SET nome = '{}', uri = '{}', img = '{}', usuario_id = {} WHERE id = {};".format(categoria['nome'], categoria['uri'], categoria['img'], categoria['usuario_id'], categoria['id'])  # faz monta q query
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