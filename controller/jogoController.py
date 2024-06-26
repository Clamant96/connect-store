from connectStore import app
from repository.jogoRepository import *
from flask import jsonify, request

from repository.upload import uploadImagem, renderImagem
from utils import validaToken

@app.route('/jogo/', methods=['GET'])
def getAllJogos():
    data = request.headers.get('Authorization')

    if data:

        if validaToken(data):
            try:
                return jsonify(findAllJogo())
            except:
                return None

        return None

    return 'Acesso nao autorizado'

@app.route('/jogo/jogos-consoles/', methods=['GET'])
def getAllJogosConsoles():
    data = request.headers.get('Authorization')

    if data:

        if validaToken(data):
            return jsonify(findAllJogosConsoles())

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
            # return postJogo(data)
            return postJogoObjCompleto(data)

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

@app.route('/jogo/associa-dados/jogo-id/<int:idJogo>/console-id/<int:idConsole>', methods=['GET'])
def postAssociaConsoleEmJogo(idJogo, idConsole):
    token = request.headers.get('Authorization')

    if token:

        if validaToken(token):
            return postConsoleEmJogo(idJogo, idConsole)

        return None

    return 'Acesso nao autorizado'

@app.route('/jogo/upload', methods=['POST'])
def postUploadImagemJogo() -> str | None:
    token = request.headers.get('Authorization')

    if token:

        if validaToken(token):

            retorno = uploadImagem(request.files['file'], 'jogos')

            if validaToken(token) and retorno is not None:
                return retorno

        return 'Ocorreu um erro ao tentar salvar o aquivo no repositorio.'
    else:
        return 'Acesso nao autorizado'

@app.route('/jogo/render/<pasta>/<nome>', methods=['GET'])
def renderImageJogoByName(pasta, nome) -> str | None:

    return renderImagem(pasta, nome)