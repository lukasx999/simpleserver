import logging
import socketserver

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
            self.data = self.request.recv(1024).strip()
            logger.debug("Received from %s: %s", self.client_address[0], self.data)
            self.request.sendall(self.data.upper() + b"\n")
            if self.data.upper() == b"QUIT":
                break
        logger.debug("Client %s left", self.client_address[0])


def main():
    HOST, PORT = "0.0.0.0", 9999

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        logger.debug(f"Listening to {HOST}:{PORT}")
        server.serve_forever()


if __name__ == "__main__":
    main()
