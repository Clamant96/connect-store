from connectStore import app
from repository.jogoRepository import *
from flask import jsonify, request
from utils import validaToken

@app.route('/jogo/', methods=['GET'])
def getAllJogos():
    data = request.headers.get('Authorization')

    if data:

        if validaToken(data):
            return jsonify(findAllJogo())

        return None

    return 'Acesso nao autorizado'



@app.route('/jogo/<int:id>', methods=['GET'])
def getByIdJogos(id: int):
    data = request.headers.get('Authorization')

    if data:

        if validaToken(data):
            return jsonify(findByIdJogo(id))

        return None

    return 'Acesso nao autorizado'

@app.route('/jogo/criar-jogo', methods=['POST'])
def criarJogos():
    data = request.get_json(silent=True)
    token = request.headers.get('Authorization')

    if token:

        if validaToken(token):
            return postJogo(data)

        return None

    return 'Acesso nao autorizado'

@app.route('/jogo/atualizar-jogo', methods=['PUT'])
def atualizarJogos():
    data = request.get_json(silent=True)
    token = request.headers.get('Authorization')

    if token:

        if validaToken(token):
            return putJogo(data)

        return None

    return 'Acesso nao autorizado'

@app.route('/jogo/deletar-jogo/<int:id>', methods=['DELETE'])
def deletarJogos(id):
    token = request.headers.get('Authorization')

    if token:

        if validaToken(token):
            return deleteByIdJogo(id)

        return None

    return 'Acesso nao autorizado'
