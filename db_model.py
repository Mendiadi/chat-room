
class DBModel:

    def to_json(self) -> dict:
        return self.__dict__