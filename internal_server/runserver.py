from webserver import WebServer


def main():
    ws = WebServer()
    ws.serve("127.0.0.1", 9080)


if __name__ == '__main__':
    main()

