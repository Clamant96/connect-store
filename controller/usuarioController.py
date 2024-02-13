from connectStore import app
from repository.usuarioRepository import *
from models.usuario import *
from flask import jsonify, request, session
from utils import validaToken

@app.route('/usuario/', methods=['GET'])
def getAllUsuarios():
    data = request.headers.get('Authorization')

    if data:

        if validaToken(data):
            return jsonify(findAllUsuarios())

        return None

    return 'Acesso nao autorizado'

@app.route('/usuario/<int:id>', methods=['GET'])
def getByIdUsuario(id: int):
    data = request.headers.get('Authorization')

    if data:

        if validaToken(data):
            return jsonify(findByIdUsuario(id))

        return None

    return 'Acesso nao autorizado'

@app.route('/usuario/criar-usuario', methods=['POST'])
def criarUsuario():
    data = request.get_json(silent=True)

    return postUsuario(data)

@app.route('/usuario/atualizar-usuario', methods=['PUT'])
def atualizarUsuario():
    data = request.get_json(silent=True)
    token = request.headers.get('Authorization')

    if token:

        if validaToken(token):
            return putUsuario(data)

        return None

    return 'Acesso nao autorizado'

@app.route('/usuario/deletar-usuario/<int:id>', methods=['DELETE'])
def deletarUsuario(id):
    token = request.headers.get('Authorization')

    if token:

        if validaToken(token):
            return deleteByIdUsuario(id)

        return None

    return 'Acesso nao autorizado'

@app.route('/usuario/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)

    return loginUsuario(data)
