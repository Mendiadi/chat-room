import dataclasses

from db_model import DBModel
@dataclasses.dataclass
class User(DBModel):

    username:str
    password:str



