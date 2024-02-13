from connectStore import app
from repository.jogoRepository import *
from flask import jsonify, request

@app.route('/jogo/', methods=['GET'])
def getAllJogos():
    jogos = findAllJogo()

    return jsonify(jogos)

@app.route('/jogo/<int:id>', methods=['GET'])
def getByIdJogos(id: int):
    jogo = findByIdJogo(id)

    return jsonify(jogo)

@app.route('/jogo/criar-jogo', methods=['POST'])
def criarJogos():
    data = request.get_json(silent=True)

    return postJogo(data)

@app.route('/jogo/atualizar-jogo', methods=['PUT'])
def atualizarJogos():
    data = request.get_json(silent=True)

    return putJogo(data)

@app.route('/jogo/deletar-jogo/<int:id>', methods=['DELETE'])
def deletarJogos(id):
    return deleteByIdJogo(id)
