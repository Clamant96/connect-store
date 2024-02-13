from connectStore import app
from repository.usuarioRepository import *
from models.usuario import *
from flask import jsonify, request, session

@app.route('/', methods=['GET'])
def getAllUsuarios():
    usuarios = findAllUsuarios()

    return jsonify(usuarios)

@app.route('/<int:id>', methods=['GET'])
def getByIdUsuario(id: int):
    usuario = findByIdUsuario(id)

    return jsonify(usuario)

@app.route('/criar-usuario', methods=['POST'])
def criarUsuario():
    data = request.get_json(silent=True)

    return postUsuario(data)

@app.route('/atualizar-usuario', methods=['PUT'])
def atualizarUsuario():
    data = request.get_json(silent=True)

    return putUsuario(data)

@app.route('/deletar-usuario/<int:id>', methods=['DELETE'])
def deletarUsuario(id):
    return deleteByIdUsuario(id)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)

    return loginUsuario(data)
