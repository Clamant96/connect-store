from pydantic import BaseModel
from models import console, jogo, usuario

class Categoria(BaseModel):
    id: int
    nome: str
    uri: str
    img: str
    usuario_id: int

class CategoriaRequest(BaseModel):
    id: int
    nome: str
    uri: str
    usuario_id: int
    file: str
    consoles: list
    jogos: list
    usuarios: list

