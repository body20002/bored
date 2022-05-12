from pydantic import BaseModel


class FactBase(BaseModel):
    fact: str
    source: str

    class Config:
        orm_mode = True


class Fact(FactBase):
    id: int


class FactInfo(FactBase):
    pass
