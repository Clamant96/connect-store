from connectStore import app
from repository.usuarioRepository import *
from models.usuario import *
from flask import jsonify, request, session

@app.route('/usuario/', methods=['GET'])
def getAllUsuarios():
    usuarios = findAllUsuarios()

    return jsonify(usuarios)

@app.route('/usuario/<int:id>', methods=['GET'])
def getByIdUsuario(id: int):
    usuario = findByIdUsuario(id)

    return jsonify(usuario)

@app.route('/usuario/criar-usuario', methods=['POST'])
def criarUsuario():
    data = request.get_json(silent=True)

    return postUsuario(data)

@app.route('/usuario/atualizar-usuario', methods=['PUT'])
def atualizarUsuario():
    data = request.get_json(silent=True)

    return putUsuario(data)

@app.route('/usuario/deletar-usuario/<int:id>', methods=['DELETE'])
def deletarUsuario(id):
    return deleteByIdUsuario(id)

@app.route('/usuario/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)

    return loginUsuario(data)
