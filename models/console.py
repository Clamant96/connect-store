from pydantic import BaseModel

class Console(BaseModel):
    id: int
    nome: str
    usuario_id: int