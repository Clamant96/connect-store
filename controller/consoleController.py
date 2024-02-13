
from connectStore import app
from repository.consoleRepository import  *
from flask import jsonify, request

@app.route('/console/', methods=['GET'])
def getAllConsoles():
    consoles = findAllConsole()

    return jsonify(consoles)

@app.route('/console/<int:id>', methods=['GET'])
def getByIdConsole(id: int):
    console = findByIdConsole(id)

    return jsonify(console)

@app.route('/console/criar-console', methods=['POST'])
def criarConsole():
    data = request.get_json(silent=True)

    return postConsole(data)

@app.route('/console/atualizar-console', methods=['PUT'])
def atualizarConsole():
    data = request.get_json(silent=True)

    return putConsole(data)

@app.route('/console/deletar-console/<int:id>', methods=['DELETE'])
def deletarConsole(id):
    return deleteByIdConsole(id)