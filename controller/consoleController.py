from connectStore import app
from repository.consoleRepository import  *
from flask import jsonify, request
from utils import validaToken

@app.route('/console/', methods=['GET'])
def getAllConsoles():
    data = request.headers.get('Authorization')

    if data:

        if validaToken(data):
            return jsonify(findAllConsole())

        return None

    return 'Acesso nao autorizado'

@app.route('/console/<int:id>', methods=['GET'])
def getByIdConsole(id: int):
    data = request.headers.get('Authorization')

    if data:

        if validaToken(data):
            return jsonify(findByIdConsole(id))

        return None

    return 'Acesso nao autorizado'

@app.route('/console/criar-console', methods=['POST'])
def criarConsole():
    data = request.get_json(silent=True)
    token = request.headers.get('Authorization')

    if token:

        if validaToken(token):
            return postConsole(data)

        return None

    return 'Acesso nao autorizado'

@app.route('/console/atualizar-console', methods=['PUT'])
def atualizarConsole():
    data = request.get_json(silent=True)
    token = request.headers.get('Authorization')

    if token:

        if validaToken(token):
            return putConsole(data)

        return None

    return 'Acesso nao autorizado'

@app.route('/console/deletar-console/<int:id>', methods=['DELETE'])
def deletarConsole(id):
    token = request.headers.get('Authorization')

    if token:

        if validaToken(token):
            return deleteByIdConsole(id)

        return None

    return 'Acesso nao autorizado'
