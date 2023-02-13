from threading import Thread

from webserver import WebServer
from random import randint

WS_PORT = randint(8000, 9000)
WS_ADDR = "127.0.0.1"


def server():
    ws = WebServer()
    ws.serve(WS_ADDR, WS_PORT)


thread = Thread(target=server)
thread.setDaemon(True)
thread.start()


def before_all(context):
    context.connection_string = f"http://{WS_ADDR}:{WS_PORT}"
