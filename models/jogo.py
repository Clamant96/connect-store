from pydantic import BaseModel

class Jogo(BaseModel):
    id: int
    nome: str
    img: str
    preco: str
    desconto: int
    categoria_id: int
    console_id: int
    usuario_id: int
