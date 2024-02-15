from pydantic import BaseModel

class Console(BaseModel):
    id: int
    nome: str
    icone: str
    usuario_id: int