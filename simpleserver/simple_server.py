import logging
import socketserver

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


class MyTCPHandler(socketserver.BaseRequestHandler):
    clients = []

    def handle(self):
        client_address = self.client_address[0]

        self.request.sendall(b"Hi there: " + client_address.encode("utf-8"))
        self.request.sendall(b"Please enter your username: ")
        self.username = self.request.recv(1024).strip()
        self.request.sendall(b"Type 'quit' to quit.\n")

        self.clients.append(self)

        while True:
            data = self.request.recv(1024).strip()
            print(f"{self.username.decode()}: {data.decode()}")

            if data == b"quit":
                break

            for client in self.clients:
                if client is not self:
                    client.request.sendall(f"{self.username.decode()}: {data.decode()}".encode())

        print(f"Client {client_address} left")
        self.clients.remove(self)


class MyTCPServer(socketserver.ThreadingTCPServer):

    HOST, PORT = "0.0.0.0", 9999

    def __init__(self):
        self.allow_reuse_address = True
        super().__init__((MyTCPServer.HOST, MyTCPServer.PORT), MyTCPHandler)

    def serve_forever(self, poll_interval=0.5):
        print(f"Listening to: {MyTCPServer.HOST}:{MyTCPServer.PORT}\n")
        super().serve_forever(poll_interval)


def main():
    with MyTCPServer() as server:
        server.serve_forever()

if __name__ == "__main__":
    main()
