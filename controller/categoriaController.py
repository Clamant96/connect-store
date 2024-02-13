from connectStore import app
from repository.categoriaRepository import *
from flask import jsonify, request

@app.route('/categoria/', methods=['GET'])
def getAllCategoria():
    consoles = findAllCategoria()

    return jsonify(consoles)

@app.route('/categoria/<int:id>', methods=['GET'])
def getByIdCategoria(id: int):
    console = findByIdCategoria(id)

    return jsonify(console)

@app.route('/categoria/criar-categoria', methods=['POST'])
def criarCategoria():
    data = request.get_json(silent=True)

    return postCategoria(data)

@app.route('/categoria/atualizar-categoria', methods=['PUT'])
def atualizarCategoria():
    data = request.get_json(silent=True)

    return putCategoria(data)

@app.route('/categoria/deletar-categoria/<int:id>', methods=['DELETE'])
def deletarCategoria(id):
    return deleteByIdCategoria(id)