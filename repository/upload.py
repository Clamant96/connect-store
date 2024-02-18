from utils import uploadImagemRepositorio


def uploadImagem(file, pasta: str):
    retorno = uploadImagemRepositorio(file, pasta)

    if retorno is not None:
        return retorno
    else:
        return None
