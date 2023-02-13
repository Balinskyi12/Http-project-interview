from .abc import BaseWebServer,HTTPRequest,HTTPResponse
import socket
import json
import os

class HTTPMixin:
    cer: str = "\r\n"
    headers: dict = None
    content: str = None

class Request(HTTPMixin,HTTPRequest):
    def __init__(self):
        self.content = None
        self.headers = {}
        self.uri = None
        self.method = None

    def parse(self, data: bytes):
        meta, self.content = data.decode().split(self._spacer * 2)
        meta_html, *headers = meta.split(self._spacer)
        self.method, self.uri, _ = meta_html.split(" ")
        for h in headers:
            k, v = h.split(": ")
            self.headers[k] = v

class Response(HTTPMixin, HTTPResponse):
    def __int__(self):
        self.headers = {}
        self.reason = None
        self.content = None
        self.code = None
        self.request = None

    def dump(self) -> bytes:
        r = f"HTTP/1.1 {self.code} {self.reason} {self._spacer}"

        headers = self.default_headers
        headers.update(self.headers or {})

        for key, value in headers.items():
            r += f"{key}: {value}{self._spacer}"
        r += self._spacer * 2
        r += self.content or ""

        return r.encode()

    def parse(self, data: bytes):
        pass




class WebServer(BaseWebServer):
    SERVER_ADDRESS = ('127.0.0.1', 9080)


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(10)
    print('server is running')


    while True:
        connection, address = server_socket.accept()
        print("new connection from {address}".format(address=address))

        data = connection.recv(1024)
        print(str(data))

        connection.send(bytes('Hello from server!', encoding='UTF-8'))

        connection.close()

    __bytes_to_read = 1024

    _registered_routes = {
        "/": ("index", False),
        "/blog": ("blog", True),
    }

    _methods_allowed = ("POST", "GET")
    _auth_header = "AUTH"
    _template_path = "webserver/templates"
    _template_suffix = ".html.template"

    def serve(self, address: str, port: int):
        self.serve(address, port)

    def handle_connection(self, conn: socket.socket):
        try:
            request = self.request_parse(conn)
            response = self.response_construct(request)
            self.response_send(conn, response)
        except ConnectionResetError:
            conn = None
        except Exception as err:
            self.send_500_error(conn, err)
            raise err
        finally:
            if conn:
                conn.close()

    def request_parse(self, conn: socket.socket) -> HTTPRequest:
        data_bytes = self._read(conn)
        request = Request()
        request.parse(data_bytes)
        return request

    def response_construct(self, r: HTTPRequest) -> HTTPResponse:
        response = Response()
        response.request = r

        if not str(r.method).upper() in self._methods_allowed:
            response.code = 405
            response.reason = "Method Not Allowed"

        elif r.uri in self._registered_routes:
            tmpl, secured = self._registered_routes[r.uri]
            if secured and not self.is_authorised(r):
                response.code = 403
                response.reason = "Forbidden"
            else:
                response.code = 200
                response.reason = "OK"
                response.content = self.load_template(tmpl, {})
        else:
            response.code = 404
            response.reason = "Not Found"
            response.content = "Page Not Found"

        return response

    def response_send(self, conn: socket.socket, r: HTTPResponse):
        data = r.dump()
        self._send(conn, data)

    def send_500_error(self, conn: socket.socket, err: Exception):
        default_response = Response()
        default_response.code = 500
        default_response.reason = "Internal Server Error"
        default_response.content = str(err)
        data = default_response.dump()
        self._send(conn, data)

    def is_authorised(self, r: HTTPRequest) -> bool:
        headers = [h.upper() for h in r.headers]
        return self._auth_header in headers  # Super secure challenge =)

    def load_template(self, name, context):
        template_path = os.path.join(
            self._template_path, f"{name}{self._template_suffix}"
        )
        if not os.path.isfile(template_path):
            return json.dumps(context)

        with open(template_path) as fh:
            template = fh.read()

        base_template_path = os.path.join(
            self._template_path, f"base{self._template_suffix}"
        )
        with open(base_template_path) as fh:
            base_template = fh.read()
            return base_template.format(BLOCK_CONTEXT=template)