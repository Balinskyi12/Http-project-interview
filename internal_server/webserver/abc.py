import socket
from abc import ABC
from abc import abstractmethod


class BaseWebServer(ABC):

    __bytes_to_read = 1024

    @abstractmethod
    def serve(self, address: str, port: int):
        pass

    @abstractmethod
    def handle_connection(self, conn: socket.socket):
        pass


class HTTPRequest(ABC):
    uri: str = None
    method: str = None

    @abstractmethod
    def parse(self, data: bytes):
        pass


class HTTPResponse(ABC):
    code: int = None
    request: HTTPRequest = None
    reason: str = None
    default_headers: dict = {
        "Content-Type": "text/html; charset=utf-8",
        "Server": "TOHT Simple Server",
    }

    @abstractmethod
    def dump(self) -> bytes:
        pass
