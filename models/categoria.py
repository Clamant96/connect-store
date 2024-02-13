from pydantic import BaseModel


class Categoria(BaseModel):
    id: int
    nome: str
    usuario_id: int