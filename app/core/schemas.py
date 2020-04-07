from app.core.rwmodel import RWModel


class RWSchema(RWModel):
    class Config(RWModel.Config):
        orm_mode = True
