from pydantic import BaseModel


class Role(BaseModel):
    id: int
    code: str
    name: str

    class Config:
        orm_mode = True


class RoleCreate(BaseModel):
    code: str
    name: str

