from connectStore import app
from repository.categoriaRepository import *
from flask import jsonify, request
from utils import validaToken
from repository.upload import uploadImagem, renderImagem

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

@app.route('/categoria/order-by-limit-1', methods=['GET'])
def getByCategoriaOrderByIdLimit1():
    data = request.headers.get('Authorization')

    if data:

        if validaToken(data):
            return jsonify(findByIdCategoriaLimit1())

        return None

    return 'Acesso nao autorizado'

@app.route('/categoria/all-jogos-com-console-usuario-e-categoria', methods=['GET'])
def getAllJogosComSeusConsolesEUsuarioCategoria():
    data = request.headers.get('Authorization')

    if data:

        if validaToken(data):
            return jsonify(findAllJogosComSeusConsolesEUsuarioCategoria())

        return None

    return 'Acesso nao autorizado'

@app.route('/categoria/all-jogos-com-console-usuario-e-categoria-many-to-many-jogos', methods=['GET'])
def getAllJogosComSeusConsolesEUsuarioCategoriaManyToManyJogos():
    data = request.headers.get('Authorization')

    if data:

        if validaToken(data):
            return jsonify(findAllJogosComSeusConsolesEUsuarioCategoriaManyToManyJogos())

        return None

    return 'Acesso nao autorizado'

@app.route('/categoria/all-jogos-categoria/<int:id>', methods=['GET'])
def getAllJogosCategoriaById(id: int):
    data = request.headers.get('Authorization')

    if data:

        if validaToken(data):
            return jsonify(findAllJogosCategoriaById(id))

        return None

    return 'Acesso nao autorizado'

@app.route('/categoria/all-jogos-com-console-usuario-e-categoria-by-id-many-to-many-jogos/<int:id>', methods=['GET'])
def getAllJogosComSeusConsolesEUsuarioCategoriaByIdManyToManyJogos(id: int):
    data = request.headers.get('Authorization')

    if data:

        if validaToken(data):
            return jsonify(findAllJogosComSeusConsolesEUsuarioCategoriaByIdManyToManyJogos(id))

        return None

    return 'Acesso nao autorizado'

@app.route('/categoria/all-jogos-categoria-uri/<uri>', methods=['GET'])
def getAllJogosCategoriaByUri(uri: str):
    data = request.headers.get('Authorization')

    if data:

        if validaToken(data):
            return jsonify(findAllJogosCategoriaByUri(uri))

        return None

    return 'Acesso nao autorizado'

@app.route('/categoria/all-jogos-com-console-usuario-e-categoria-by-uri-many-to-many-jogos/<uri>', methods=['GET'])
def getAllJogosComSeusConsolesEUsuarioCategoriaByUriManyToManyJogos(uri: str):
    data = request.headers.get('Authorization')

    if data:

        if validaToken(data):
            return jsonify(findAllJogosComSeusConsolesEUsuarioCategoriaByUriManyToManyJogos(uri))

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

@app.route('/categoria/associa-dados/categoria-id/<int:idCategoria>/console-id/<int:idConsole>', methods=['GET'])
def postAssociaConsoleEmCategoria(idCategoria, idConsole):
    token = request.headers.get('Authorization')

    if token:

        if validaToken(token):
            return postConsoleEmCategoria(idCategoria, idConsole)

        return None

    return 'Acesso nao autorizado'

@app.route('/categoria/cadastrar-categoria', methods=['POST'])
def postCategoriaObj():
    data = request.get_json(silent=True)

    print('DATA postCategoriaObj(): ', data)

    token = request.headers.get('Authorization')

    if token:

        if validaToken(token):
            return postCategoriaObjCompleto(data)

        return None

    return 'Acesso nao autorizado'

@app.route('/categoria/atualizar-categoria-obj', methods=['PUT'])
def putCategoriaObj():
    data = request.get_json(silent=True)

    print('DATA putCategoriaObj(): ', data)

    token = request.headers.get('Authorization')

    if token:

        if validaToken(token):
            return putCategoriaObjCompleto(data)

        return None

    return 'Acesso nao autorizado'

@app.route('/categoria/deletar-categoria-obj/<int:id>', methods=['DELETE'])
def deletarCategoriaObj(id):
    token = request.headers.get('Authorization')

    if token:

        if validaToken(token):
            return deleteByIdCategoriaObj(id)

        return None

    return 'Acesso nao autorizado'

@app.route('/categoria/upload', methods=['POST'])
def postUploadImagem() -> str | None:
    token = request.headers.get('Authorization')

    if token:

        if validaToken(token):

            retorno = uploadImagem(request.files['file'], 'categorias')

            if validaToken(token) and retorno is not None:
                return retorno

        return 'Ocorreu um erro ao tentar salvar o aquivo no repositorio.'
    else:
        return 'Acesso nao autorizado'

@app.route('/categoria/render/<pasta>/<nome>', methods=['GET'])
def renderImageByName(pasta, nome) -> str | None:

    return renderImagem(pasta, nome)
