from utils import uploadImagemRepositorio
from flask import send_from_directory


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
