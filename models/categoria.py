from pydantic import BaseModel


class Categoria(BaseModel):
    id: int
    nome: str
    uri: str
    img: str
    usuario_id: int