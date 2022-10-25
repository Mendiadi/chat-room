import socket

from schemas import *
from communication import ConnectionProtocol


class Networking(ConnectionProtocol):
    def __init__(self, host, port):
        super().__init__(host, port)
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect((self.host, self.port))
        self.logged_name = None

    def request(self, method: str, data: [dict, object]):
        if not isinstance(data, dict) and not isinstance(data, str):
            data = data.to_json()
        if self.logged_name:
            data = {'name': self.logged_name, 'msg': data}
        data_ = NativeFormat(method, data)

        self._client.send(data_.pack())

    @property
    def client(self) -> socket.socket:
        return self._client

