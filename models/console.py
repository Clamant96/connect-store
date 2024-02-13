from pydantic import BaseModel
from models.usuario import Usuario

class Console(BaseModel):
    id: int
    nome: str
    usuario_id: int