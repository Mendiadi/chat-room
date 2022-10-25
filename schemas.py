import json

class RequestsMethods:
    login = "login"
    register = "register"
    message = "msg"

class ErrorInfo:
    USER_NOT_FOUND = "username not found"
    PASSWORD_NOT_MATCH = "password not match"
    USER_EXISTS = "username exists"

class NativeFormat:
    def __init__(self, type: str, data: dict):
        self.type = type
        self.data = data

    def pack(self):
        return json.dumps(self.__dict__).encode()

class Schemas:
    def __init__(self,type):
        self.type = type
    def prepare_request(self) -> NativeFormat:
        return NativeFormat(self.type,self.__dict__)



class ErrorSchemas(Schemas):
    def __init__(self,type,reason,info):
        super().__init__(type)
        self.reason = reason
        self.info = info