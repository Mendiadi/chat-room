
class DBModel:

    def to_json(self) -> dict:
        return self.__dict__

import dataclasses



@dataclasses.dataclass
class User(DBModel):

    username:str
    password:str


