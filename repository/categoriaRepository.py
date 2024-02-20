from typing import Any

from db import acessando_base
from models.categoria import *
from utils import converteDictEmJsonAll
from connectStore import findByIdConsole
from repository.jogoRepository import findByIdJogo
from repository.upload import deletaImagem

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


def findByIdCategoria(id: int) -> Categoria | None:
    con = acessando_base()  # faz a conexao com o banco
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
    cursor.execute(query)  # faz a busca no banco

    result = converteDictEmJsonAll(cursor)  # faz a busca no banco e formata o retorno e retorna somente 1 dado

    if con.is_connected():
        con.close()
        cursor.close()

    if result[0]['categorias'] != None:
        return json.loads(result[0]['categorias'])[0]  # retorna somente o objeto JSON
    else:
        return None


def findByIdCategoriaLimit1() -> Categoria | None:
    con = acessando_base()  # faz a conexao com o banco
    query = '''
        SELECT
          JSON_PRETTY(
              JSON_OBJECT('id', c.id, 'nome', c.nome, 'uri', c.uri, 'img', c.img)) AS categorias
            FROM
                connect_store.categoria c
        ORDER BY c.id DESC limit 1;
    '''
    cursor = con.cursor()
    cursor.execute(query)  # faz a busca no banco

    result = converteDictEmJsonAll(cursor)  # faz a busca no banco e formata o retorno e retorna somente 1 dado

    if con.is_connected():
        con.close()
        cursor.close()

    if result[0]['categorias'] != None:
        return json.loads(result[0]['categorias'])  # retorna somente o objeto JSON
    else:
        return None


def findByNomeCategoria(nome: str) -> Categoria | None:
    con = acessando_base()  # faz a conexao com o banco
    query = "SELECT * FROM categoria WHERE nome = '{}'".format(nome)  # faz monta q query
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


def findAllJogosComSeusConsolesEUsuarioCategoria() -> Categoria | None:
    con = acessando_base()  # faz a conexao com o banco
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
    cursor.execute(query)  # faz a busca no banco

    result = converteDictEmJsonAll(cursor)  # faz a busca no banco e formata o retorno e retorna somente 1 dado

    print('conexao ativa? ', con.is_connected())

    if con.is_connected():
        print('Conexao finalizada!')
        con.close()
        cursor.close()

    if result[0]['categorias'] != None:
        return json.loads(result[0]['categorias'])  # retorna somente o objeto JSON
    else:
        return None


def findAllJogosComSeusConsolesEUsuarioCategoriaManyToManyJogos() -> Categoria | None:
    con = acessando_base()  # faz a conexao com o banco
    # query = "SELECT * FROM categoria WHERE id = {}".format(id)  # faz monta q query
    query = '''
        SELECT 
                JSON_PRETTY(
                  JSON_ARRAYAGG(JSON_OBJECT('id', c.id, 'nome', c.nome, 'uri', c.uri, 'img', c.img, 'jogos', cs.jogos, 'usuarios', s.usuarios, 'consoles', csn.consoles))) AS categorias
            FROM 
                connect_store.categoria AS c 
                
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
                
                left join (
                    SELECT cc.categoria_id, 
                        JSON_ARRAYAGG(JSON_OBJECT('id', j.id, 'nome', j.nome, 'img', j.img, 'preco', j.preco, 'desconto', j.desconto, 'consoles', jcsn.consoles)) AS jogos
                    FROM 
                        connect_store.categoria AS cat RIGHT JOIN connect_store.categoria_jogo AS cc ON cc.categoria_id = cat.id LEFT JOIN connect_store.jogo AS j ON cc.jogo_id = j.id 
                            
                            -- ADICIONA OS CONSOLES NO OBJ JOGO
                                left join (
                                    SELECT jogocons.jogo_id, 
                                        JSON_ARRAYAGG(JSON_OBJECT('id', cons.id, 'nome', cons.nome, 'icone', cons.icone)) AS consoles
                                    FROM 
                                        connect_store.console AS cons 
                                            left join 
                                                connect_store.jogo_console AS jogocons 
                                            ON cons.id = jogocons.console_id 
                                    GROUP BY jogocons.jogo_id) jcsn 
                                ON j.id = jcsn.jogo_id
                            
                GROUP BY cc.categoria_id) cs ON cs.categoria_id = c.id;
    '''
    cursor = con.cursor()
    cursor.execute(query)  # faz a busca no banco

    result = converteDictEmJsonAll(cursor)  # faz a busca no banco e formata o retorno e retorna somente 1 dado

    print('conexao ativa? ', con.is_connected())

    if con.is_connected():
        print('Conexao finalizada!')
        con.close()
        cursor.close()

    if result[0]['categorias'] != None:
        return json.loads(result[0]['categorias'])  # retorna somente o objeto JSON
    else:
        return None


def findAllJogosCategoriaById(id: int) -> Categoria | None:
    con = acessando_base()  # faz a conexao com o banco
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
    cursor.execute(query)  # faz a busca no banco

    result = converteDictEmJsonAll(cursor)  # faz a busca no banco e formata o retorno e retorna somente 1 dado

    if con.is_connected():
        con.close()
        cursor.close()

    if result[0]['categorias'] != None:
        return json.loads(result[0]['categorias'])[0]  # retorna somente o objeto JSON
    else:
        return None


def findAllJogosComSeusConsolesEUsuarioCategoriaByIdManyToManyJogos(id: int) -> Categoria | None:
    con = acessando_base()  # faz a conexao com o banco
    # query = "SELECT * FROM categoria WHERE id = {}".format(id)  # faz monta q query
    query = '''
        SELECT 
                JSON_PRETTY(
                  JSON_ARRAYAGG(JSON_OBJECT('id', c.id, 'nome', c.nome, 'uri', c.uri, 'img', c.img, 'jogos', cs.jogos, 'usuarios', s.usuarios, 'consoles', csn.consoles))) AS categorias
            FROM 
                connect_store.categoria AS c 

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

                left join (
                    SELECT cc.categoria_id, 
                        JSON_ARRAYAGG(JSON_OBJECT('id', j.id, 'nome', j.nome, 'img', j.img, 'preco', j.preco, 'desconto', j.desconto, 'consoles', jcsn.consoles)) AS jogos
                    FROM 
                        connect_store.categoria AS cat RIGHT JOIN connect_store.categoria_jogo AS cc ON cc.categoria_id = cat.id LEFT JOIN connect_store.jogo AS j ON cc.jogo_id = j.id 

                            -- ADICIONA OS CONSOLES NO OBJ JOGO
                                left join (
                                    SELECT jogocons.jogo_id, 
                                        JSON_ARRAYAGG(JSON_OBJECT('id', cons.id, 'nome', cons.nome, 'icone', cons.icone)) AS consoles
                                    FROM 
                                        connect_store.console AS cons 
                                            left join 
                                                connect_store.jogo_console AS jogocons 
                                            ON cons.id = jogocons.console_id 
                                    GROUP BY jogocons.jogo_id) jcsn 
                                ON j.id = jcsn.jogo_id

                GROUP BY cc.categoria_id) cs ON cs.categoria_id = c.id
            WHERE c.id = {};
    '''.format(id)
    cursor = con.cursor()
    cursor.execute(query)  # faz a busca no banco

    result = converteDictEmJsonAll(cursor)  # faz a busca no banco e formata o retorno e retorna somente 1 dado

    print('conexao ativa? ', con.is_connected())

    if con.is_connected():
        print('Conexao finalizada!')
        con.close()
        cursor.close()

    if result[0]['categorias'] != None:
        return json.loads(result[0]['categorias'])[0]  # retorna somente o objeto JSON
    else:
        return None


def findAllJogosCategoriaByUri(uri: str) -> Categoria | None:
    con = acessando_base()  # faz a conexao com o banco
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
    cursor.execute(query)  # faz a busca no banco

    result = converteDictEmJsonAll(cursor)  # faz a busca no banco e formata o retorno e retorna somente 1 dado

    if con.is_connected():
        con.close()
        cursor.close()

    if result[0]['categorias'] != None:
        return json.loads(result[0]['categorias'])[0]  # retorna somente o objeto JSON
    else:
        return None


def findAllJogosComSeusConsolesEUsuarioCategoriaByUriManyToManyJogos(uri: str) -> Categoria | None:
    con = acessando_base()  # faz a conexao com o banco
    # query = "SELECT * FROM categoria WHERE id = {}".format(id)  # faz monta q query
    query = '''
        SELECT 
                JSON_PRETTY(
                  JSON_ARRAYAGG(JSON_OBJECT('id', c.id, 'nome', c.nome, 'uri', c.uri, 'img', c.img, 'jogos', cs.jogos, 'usuarios', s.usuarios, 'consoles', csn.consoles))) AS categorias
            FROM 
                connect_store.categoria AS c 

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

                left join (
                    SELECT cc.categoria_id, 
                        JSON_ARRAYAGG(JSON_OBJECT('id', j.id, 'nome', j.nome, 'img', j.img, 'preco', j.preco, 'desconto', j.desconto, 'consoles', jcsn.consoles)) AS jogos
                    FROM 
                        connect_store.categoria AS cat RIGHT JOIN connect_store.categoria_jogo AS cc ON cc.categoria_id = cat.id LEFT JOIN connect_store.jogo AS j ON cc.jogo_id = j.id 

                            -- ADICIONA OS CONSOLES NO OBJ JOGO
                                left join (
                                    SELECT jogocons.jogo_id, 
                                        JSON_ARRAYAGG(JSON_OBJECT('id', cons.id, 'nome', cons.nome, 'icone', cons.icone)) AS consoles
                                    FROM 
                                        connect_store.console AS cons 
                                            left join 
                                                connect_store.jogo_console AS jogocons 
                                            ON cons.id = jogocons.console_id 
                                    GROUP BY jogocons.jogo_id) jcsn 
                                ON j.id = jcsn.jogo_id

                GROUP BY cc.categoria_id) cs ON cs.categoria_id = c.id
            WHERE c.uri = '{}';
    '''.format(uri)
    cursor = con.cursor()
    cursor.execute(query)  # faz a busca no banco

    result = converteDictEmJsonAll(cursor)  # faz a busca no banco e formata o retorno e retorna somente 1 dado

    print('conexao ativa? ', con.is_connected())

    if con.is_connected():
        print('Conexao finalizada!')
        con.close()
        cursor.close()

    if result[0]['categorias'] != None:
        return json.loads(result[0]['categorias'])[0]  # retorna somente o objeto JSON
    else:
        return None


def postCategoria(categoria: Categoria) -> Categoria | str:
    if findByNomeCategoria(categoria['nome']) == None:
        con = acessando_base()  # faz a conexao com o banco
        query = "INSERT INTO categoria (nome, uri, img, usuario_id) VALUES ('{}', '{}', '{}', {});".format(
            categoria['nome'], categoria['uri'], categoria['img'], categoria['usuario_id'])  # faz monta q query
        cursor = con.cursor()
        result = cursor.execute(query)  # faz a busca no banco
        con.commit()  # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        return findByNomeCategoria(categoria['nome'])

    return 'Categoria ja existe na base.'


def postCategoriaObjCompleto(categoria: CategoriaRequest) -> Categoria | str:
    print('postCategoriaObjCompleto(): ', categoria)

    categoria['uri'] = str(categoria['uri']).replace(' ', '-')

    if findByNomeCategoria(categoria['nome']) == None:

        con = acessando_base()  # faz a conexao com o banco
        query = "INSERT INTO categoria (nome, uri, img, usuario_id) VALUES ('{}', '{}', '{}', {});".format(
            categoria['nome'], categoria['uri'], categoria['img'], categoria['usuario_id'])  # faz monta q query
        cursor = con.cursor()
        result = cursor.execute(query)  # faz a busca no banco
        con.commit()  # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        categoriaCriada = findByIdCategoriaLimit1()

        print('categoriaCriada: ', categoriaCriada)

        print('categoriaCriada NOME: ', categoriaCriada['nome'])
        print('categoria NOME: ', categoria['nome'])

        if categoriaCriada['nome'] == categoria['nome']:
            print('CATEGORIA CADASTRADA E LOCALIZADA, AGORA SERA FEIRA A ASSOCIACAO MANY-TO-MANY')

            if categoria['consoles']:

                print('categoria CONSOLES', categoria['consoles'])

                for console in categoria['consoles']:

                    print('console: ', console)

                    if categoriaCriada['id']:
                        postConsoleEmCategoria(categoriaCriada['id'], console['id'])

            if categoria['jogos']:

                print('categoria JOGOS', categoria['jogos'])

                for jogo in categoria['jogos']:

                    print('jogo: ', jogo)

                    if categoriaCriada['id']:
                        postJogoEmCategoria(categoriaCriada['id'], jogo['id'])

            return findByNomeCategoria(categoria['nome'])

        return 'Categoria ja existe na base.'


def postConsoleEmCategoria(idCategoria: int, idConsole: int) -> str:
    if findByIdCategoria(idCategoria) != None and findByIdConsole(idConsole) != None:
        con = acessando_base()  # faz a conexao com o banco
        query = "INSERT INTO connect_store.categoria_console (categoria_id, console_id) VALUES ('{}', {});".format(
            idCategoria, idConsole)
        cursor = con.cursor()
        result = cursor.execute(query)  # faz a busca no banco
        con.commit()  # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        return 'Associacao realizada com sucesso!'

    return 'Nao foi possivel associar os dados.'


def postJogoEmCategoria(idCategoria: int, idJogo: int) -> str:
    if findByIdCategoria(idCategoria) != None and findByIdJogo(idJogo) != None:
        con = acessando_base()  # faz a conexao com o banco
        query = "INSERT INTO connect_store.categoria_jogo (categoria_id, jogo_id) VALUES ('{}', {});".format(
            idCategoria, idJogo)
        cursor = con.cursor()
        result = cursor.execute(query)  # faz a busca no banco
        con.commit()  # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        return 'Associacao realizada com sucesso!'

    return 'Nao foi possivel associar os dados.'


def putCategoria(categoria: Categoria) -> Categoria | None:
    if findByIdCategoria(categoria['id']) != None:
        con = acessando_base()  # faz a conexao com o banco
        query = "UPDATE categoria SET nome = '{}', uri = '{}', img = '{}', usuario_id = {} WHERE id = {};".format(
            categoria['nome'], categoria['uri'], categoria['img'], categoria['usuario_id'],
            categoria['id'])  # faz monta q query
        cursor = con.cursor()
        cursor.execute(query)  # faz a busca no banco
        con.commit()  # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        return findByIdCategoria(categoria['id'])

    return None


def putCategoriaObjCompleto(categoria: Categoria) -> Categoria | None:
    if findByIdCategoria(categoria['id']) != None:

        con = acessando_base()  # faz a conexao com o banco
        query = "UPDATE categoria SET nome = '{}', uri = '{}', img = '{}', usuario_id = {} WHERE id = {};".format(
            categoria['nome'], categoria['uri'], categoria['img'], categoria['usuario_id'],
            categoria['id'])  # faz monta q query
        cursor = con.cursor()
        cursor.execute(query)  # faz a busca no banco
        con.commit()  # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        if deleteConsolesByIdCategoria(categoria['id']) != None:
            if categoria['consoles']:

                for console in categoria['consoles']:

                    print('console: ', console)

                    if categoria['id']:
                        postConsoleEmCategoria(categoria['id'], console['id'])

        if deleteJogosByIdCategoria(categoria['id']) != None:

            if categoria['jogos']:

                for jogo in categoria['jogos']:

                    print('jogo: ', jogo)

                    if categoria['id']:
                        postJogoEmCategoria(categoria['id'], jogo['id'])

        return findByIdCategoria(categoria['id'])

    return None


def deleteByIdCategoria(id: int) -> str:
    if findByIdCategoria(id) != None:
        con = acessando_base()  # faz a conexao com o banco
        query = "DELETE FROM categoria WHERE id = {};".format(id)  # faz monta q query

        cursor = con.cursor()
        cursor.execute(query)  # faz a busca no banco
        con.commit()  # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        return 'Categoria deletada com sucesso!'

    return 'Nao foi possivel excluir a categoria da base, pois ele nao foi localizado.'


def deleteByIdCategoriaObj(id: int) -> str:
    categoria = findByIdCategoria(id)
    if findByIdCategoria(id) != None:

        print('deleteByIdCategoriaObj()')

        # DEVIDO AOS RELACIONAMENTOS DAS TANELAS, TEMOS QUE DELETAR ELES ANTES DE DELETAR O OBJETO PRINCIPAL
        if deleteConsolesByIdCategoria(id) != '':
            print(f'Consoles excluidos da categoria: {id}')

        if deleteJogosByIdCategoria(id) != '':
            print(f'Jogos excluidos da categoria: {id}')

        if deletaImagem('categorias', categoria['img']) != "":
            print(f'Imagem excluida com sucesso: {categoria['img']}')

        con = acessando_base()  # faz a conexao com o banco
        query = "DELETE FROM connect_store.categoria WHERE id = {};".format(id)  # faz monta q query

        cursor = con.cursor()
        cursor.execute(query)  # faz a busca no banco
        con.commit()  # registrar os dados no banco

        if con.is_connected():
            con.close()
            cursor.close()

        return 'Categoria deletada com sucesso!'

    return 'Nao foi possivel excluir a categoria da base, pois ele nao foi localizado.'


def deleteJogosByIdCategoria(id: int) -> str:
    con = acessando_base()  # faz a conexao com o banco
    query = "DELETE FROM connect_store.categoria_jogo AS cj WHERE cj.categoria_id = {};".format(id)  # faz monta q query

    cursor = con.cursor()
    cursor.execute(query)  # faz a busca no banco
    con.commit()  # registrar os dados no banco

    if con.is_connected():
        con.close()
        cursor.close()

    return 'Jogos removidos da categoria com sucesso!'


def deleteConsolesByIdCategoria(id: int) -> str:
    con = acessando_base()  # faz a conexao com o banco
    query = "DELETE FROM connect_store.categoria_console AS cj WHERE cj.categoria_id = {};".format(
        id)  # faz monta q query

    cursor = con.cursor()
    cursor.execute(query)  # faz a busca no banco
    con.commit()  # registrar os dados no banco

    if con.is_connected():
        con.close()
        cursor.close()

    return 'Consoles removidos da categoria com sucesso!'
