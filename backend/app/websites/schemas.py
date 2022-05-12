from pydantic import BaseModel


class WebsiteBase(BaseModel):
    url: str
    description: str

    class Config:
        orm_mode = True


class Website(WebsiteBase):
    id: int


class WebsiteIn(WebsiteBase):
    pass
