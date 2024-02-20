from utils import uploadImagemRepositorio
from flask import send_from_directory

import os


def uploadImagem(file, pasta: str):
    retorno = uploadImagemRepositorio(file, pasta)

    if retorno is not None:
        return retorno
    else:
        return None


def renderImagem(pasta: str, nomeArquivo: str):
    print('PASTA: ', pasta)
    print('NOME: ', nomeArquivo)
    return send_from_directory(f'uploads\\{pasta}', nomeArquivo)


def deletaImagem(pasta: str, nomeArquivo: str):
    print('PASTA: ', pasta)
    print('NOME: ', nomeArquivo)

    try:
        if renderImagem(pasta, nomeArquivo):
            os.remove(os.path.join(f'uploads\\{pasta}', nomeArquivo))

            if renderImagem(pasta, nomeArquivo):
                return "Imagem excluida com sucesso!"

    except:
        return None
