from connectStore import app
from repository.categoriaRepository import *
from flask import jsonify, request
from utils import validaToken

@app.route('/categoria/', methods=['GET'])
def getAllCategoria():
    data = request.headers.get('Authorization')

    if data:

        if validaToken(data):
            return jsonify(findAllCategoria())

        return None

    return 'Acesso nao autorizado'

@app.route('/categoria/<int:id>', methods=['GET'])
def getByIdCategoria(id: int):
    data = request.headers.get('Authorization')

    if data:

        if validaToken(data):
            return jsonify(findByIdCategoria(id))

        return None

    return 'Acesso nao autorizado'

@app.route('/categoria/criar-categoria', methods=['POST'])
def criarCategoria():
    data = request.get_json(silent=True)
    token = request.headers.get('Authorization')

    if token:

        if validaToken(token):
            return postCategoria(data)

        return None

    return 'Acesso nao autorizado'

@app.route('/categoria/atualizar-categoria', methods=['PUT'])
def atualizarCategoria():
    data = request.get_json(silent=True)

    token = request.headers.get('Authorization')

    if token:

        if validaToken(token):
            return putCategoria(data)

        return None

    return 'Acesso nao autorizado'


@app.route('/categoria/deletar-categoria/<int:id>', methods=['DELETE'])
def deletarCategoria(id):
    token = request.headers.get('Authorization')

    if token:

        if validaToken(token):
            return deleteByIdCategoria(id)

        return None

    return 'Acesso nao autorizado'
