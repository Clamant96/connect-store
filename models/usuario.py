from pydantic import BaseModel


class Usuario(BaseModel):
    id: int
    nome: str
    username: str
    email: str
    senha: str
    token: str
